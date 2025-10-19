import os
import shutil
import time
import random
from pathlib import Path
from multiprocessing import Pool
from datetime import datetime
import photoUtils

def copy_photo(original, aspectRatioInfo, fileName):
    destination = 'output/' + aspectRatioInfo["type"] + '/' + aspectRatioInfo["label"] + '/' + fileName
    if os.path.isfile(destination):
        fileNameParts = fileName.split('.')
        destination = 'output/' + \
                      aspectRatioInfo["type"] + \
                      '/' + \
                      aspectRatioInfo["label"] + \
                      '/' + \
                      fileNameParts[0] + \
                      ' ' + \
                      str(int(time.time())) + \
                      str(random.randrange(1, 10000)) + \
                      '.' + \
                      fileNameParts[1]
    print ('\tCreating file: ' + destination)
    shutil.copy(original, destination)

def create_aspect_dir(aspectRatioInfo):
    dirToCreate = 'output/' + aspectRatioInfo["type"] + '/' + aspectRatioInfo["label"]
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
                if photoUtils.utils.is_picture(file):
                    print(dirPath)
                    filePath = os.path.join(dirPath, file)
                    metadata = photoUtils.metadata.get_metadata(filePath)
                    aspectRatioInfo = photoUtils.metadata.get_nearest_common_aspect_ratio(metadata)

                    newFileName = photoDir + ' ' + file
                    
                    photo = (filePath, metadata, aspectRatioInfo, newFileName)
                    
                    if aspectRatioInfo["label"] in photosByAspectRatio:
                        photosByAspectRatio[aspectRatioInfo["label"]].append(photo)
                    else:
                        photosByAspectRatio[aspectRatioInfo["label"]] = [photo]
                        create_aspect_dir(aspectRatioInfo)

                    copy_photo(filePath, aspectRatioInfo, newFileName)
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
    print (datetime.now())
    directories = [r"E:\Pictures\Test"]

    start = time.time()
    if os.path.isdir('output'):
        clean_old_output()

    processingResults = []
    for directoryToCheck in directories:
        # get the arguments for the procssing function
        photoDirectories = list(map(lambda photoDir: (directoryToCheck, photoDir), os.listdir(directoryToCheck)))
        print('dirs', photoDirectories)
        with Pool(8) as p:
            processingResults.extend(p.starmap(process_directory, photoDirectories))
    end = time.time()

    photosByAspectRatio = merge_processing_results(processingResults)
    print_photos_created_stats(photosByAspectRatio)
    print ("Time taken: " + str(end - start))
        
if __name__ == "__main__":
    main()
