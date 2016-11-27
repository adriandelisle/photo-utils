import os
import subprocess
import shutil
import time
import random

def is_picture(fileName):
    acceptedFileTypes = ['.jpg', '.nef']
    for fileType in acceptedFileTypes:
        if fileName.lower().endswith(fileType):
            return True
    return False

def get_metadata(filePath):
    ## http://stackoverflow.com/a/7006424
    CREATE_NO_WINDOW = 0x08000000
    DETACHED_PROCESS = 0x00000008
    processResult = subprocess.run(
        args = ['exiv2-0.25-win\exiv2', filePath],
        creationflags=DETACHED_PROCESS,
        universal_newlines = True,
        stdout = subprocess.PIPE)
    rawMetadata = processResult.stdout.split('\n');
    metadata = {}
    for field in rawMetadata:
        keyValue = field.split(':')
        if len(keyValue) == 2:
            metadata[keyValue[0].strip()] = keyValue[1].strip()
    return metadata

def get_aspect_ratio(metadata):
    imageSize = metadata['Image size']
    imageSize = imageSize.split('x')
    imageSize = (float(imageSize[0].strip()), float(imageSize[1].strip()))
    
    return "{:.2f}".format(imageSize[0] / imageSize[1])

def copy_photo(original, aspectRatio, fileName):
    destination = 'output/' + aspectRatio + '/' + fileName
    if os.path.isfile(destination):
        fileNameParts = fileName.split('.')
        destination = 'output/' + \
                      aspectRatio + \
                      '/' + \
                      fileNameParts[0] + \
                      ' ' + \
                      str(int(time.time())) + \
                      str(random.randrange(1, 10000)) + \
                      '.' + \
                      fileNameParts[1]
    print ('\tCreating file: ' + destination)
    shutil.copy(original, destination)

def create_aspect_dir(aspectRatio):
    dirToCreate = 'output/' + aspectRatio
    if not os.path.isdir(dirToCreate):
        print ('Creating directory: ' + dirToCreate)
        os.makedirs(dirToCreate)

def clean_old_output():
    print ('Cleaning up old output directory')
    shutil.rmtree('output')

def print_photos_created_stats(photosByAspectRatio):
    print ('Number of photos created:')
    aspectRatios = sorted(list(photosByAspectRatio.keys()))
    total = 0
    for aspectRatio in aspectRatios:
        numberOfPhotos = len(photosByAspectRatio[aspectRatio])
        print ('\tAspect Ratio: ' + aspectRatio, numberOfPhotos)
        total += numberOfPhotos
    print ('Total number of photos: ' + str(total))

def process_directory(root, photoDir):
    print ("Processing: " + os.path.join(root, photoDir))
    photosByAspectRatio = {}
    for dirPath, dirs, files in os.walk(os.path.join(root, photoDir)):
        if len(files) <= 0:
            continue

        if dirPath.lower().find("no watermark") != -1:
            for file in files:
                if is_picture(file):
                    filePath = os.path.join(dirPath, file)
                    metadata = get_metadata(filePath)
                    aspectRatio = get_aspect_ratio(metadata)

                    newFileName = photoDir + ' ' + file
                    
                    photo = (filePath, metadata, aspectRatio, newFileName)
                    
                    if aspectRatio in photosByAspectRatio:
                        photosByAspectRatio[aspectRatio].append(photo)
                    else:
                        photosByAspectRatio[aspectRatio] = [photo]
                        create_aspect_dir(aspectRatio)

                    copy_photo(filePath, aspectRatio, newFileName)
    return photosByAspectRatio

def merge_processing_results(processingResults):
    photosByAspectRatio = {}
    for result in processingResults:
        for aspect, photos in result.items():
            if aspect in photosByAspectRatio:
                photosByAspectRatio[aspect].extend(photos)
            else:
                photosByAspectRatio[aspect] = photos
    return photosByAspectRatio

def main ():
    directories = ['P:/Pictures/Nikon D5000 Photos/Photos/', 'P:/Pictures/Nikon D5000 Photos/Timelapses/']
    #directories = ['P:/Pictures/Python Test/Photos/', 'P:/Pictures/Python Test/Timelapses/']

    start = time.time()
    if os.path.isdir('output'):
        clean_old_output()

    processingResults = []
    for directoryToCheck in directories:
        for photoDir in os.listdir(directoryToCheck):
            processingResults.append(process_directory(directoryToCheck, photoDir))
    end = time.time()

    photosByAspectRatio = merge_processing_results(processingResults)
    print_photos_created_stats(photosByAspectRatio)
    print ("Time taken: " + str(end - start))
        
if __name__ == "__main__":
    main()
