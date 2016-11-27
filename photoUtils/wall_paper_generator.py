import os
import subprocess
import shutil

directories = ['P:\Pictures\Python Test\Photos\\', 'P:\Pictures\Python Test\Timelapses\\']

def is_picture (fileName):
    acceptedFileTypes = ['.jpg', '.nef']
    for fileType in acceptedFileTypes:
        if fileName.lower().endswith(fileType):
            return True
    return False

def get_metadata (filePath):
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

def get_aspect_ratio (metadata):
    imageSize = metadata['Image size']
    imageSize = imageSize.split('x')
    imageSize = (float(imageSize[0].strip()), float(imageSize[1].strip()))
    
    return "{:.2f}".format(imageSize[0] / imageSize[1])

def copy_photo(original, aspectRatio, fileName):
    destination = 'output/' + aspectRatio + '/' + fileName
    print ('\tCreating file: ' + destination)
    shutil.copy(original, destination)

def create_aspect_dir (aspectRatio):
    dirToCreate = 'output/' + aspectRatio
    print ('Creating directory: ' + dirToCreate)
    os.makedirs(dirToCreate)

def clean_old_output ():
    print ('Cleaning up old output directory')
    shutil.rmtree('output')

def print_photos_created_stats (photos):
    print ('Number of photos created:')
    for aspectRatio, photos in photos.items():
        print ('\tAspect Ratio: ' + aspectRatio, len(photos))

def main ():
    clean_old_output()
    aspectRatios = {}
    for directoryToCheck in directories:
        for photoDir in os.listdir(directoryToCheck):
            print ("Processing: " + os.path.join(directoryToCheck, photoDir))
            for dirPath, dirs, files in os.walk(os.path.join(directoryToCheck, photoDir)):
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
                            
                            if aspectRatio in aspectRatios:
                                aspectRatios[aspectRatio].append(photo)
                            else:
                                aspectRatios[aspectRatio] = [photo]
                                create_aspect_dir (aspectRatio)

                            copy_photo(filePath, aspectRatio, newFileName)

    print_photos_created_stats(aspectRatios)
        
if __name__ == "__main__":
    main()
