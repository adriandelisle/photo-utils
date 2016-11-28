import os
import time
from multiprocessing import Pool
from datetime import datetime, timedelta
import photoUtils

def process_directory(root, photoDir):
    fullDir = os.path.join(root, photoDir)
    print ("Processing: " + fullDir)
    
    dirStats = {'numberOfFiles': 0, 'duration': timedelta(0), 'size': 0}
    maybeTimelapseDirectory = os.path.join(fullDir, 'Timelapse')
    if os.path.isdir(maybeTimelapseDirectory):
        print ("\tProcessing timelapse directory: " + maybeTimelapseDirectory)
        files = os.listdir(maybeTimelapseDirectory)
        sortedFiles = sorted(files)

        photoFiles = []
        for file in sortedFiles:
            if photoUtils.utils.is_picture(file):
                filePath = os.path.join(maybeTimelapseDirectory, file)
                photoFiles.append(filePath)
                dirStats['size'] += os.path.getsize(filePath)
                dirStats['numberOfFiles'] += 1
        firstPhotoMetadata = photoUtils.metadata.get_metadata(photoFiles[0])
        firstTimestamp = photoUtils.metadata.get_created_time(firstPhotoMetadata)

        lastPhotoMetadata = photoUtils.metadata.get_metadata(photoFiles[-1])
        lastTimestamp = photoUtils.metadata.get_created_time(lastPhotoMetadata)

        dirStats['duration'] = lastTimestamp - firstTimestamp
    print ('\tDirectory stats for: ' + fullDir + '\n\t' + str(dirStats))
    return dirStats

def print_dirStats(dirStats):
    print ('Number of files: ' + str(dirStats['numberOfFiles']) + '\n' + \
           'Duration: ' + str(dirStats['duration']) + '\n' + \
           'Size: ' + photoUtils.utils.bytes_2_human_readable(dirStats['size']) + ' (Raw: ' + str(dirStats['size']) + ')')

def merge_processingResults(processingResults):
    dirStats = {'numberOfFiles': 0, 'duration': timedelta(0), 'size': 0}
    for result in processingResults:
        dirStats['numberOfFiles'] += result['numberOfFiles']
        dirStats['duration'] = dirStats['duration'] + result['duration']
        dirStats['size'] += result['size']
    return dirStats

def main ():
    print (datetime.now())
    directories = ['P:/Pictures/Nikon D5000 Photos/Timelapses/']
    #directories = ['P:/Pictures/Python Test/Timelapses/']

    start = time.time()
    processingResults = []
    for directoryToCheck in directories:
        for photoDir in os.listdir(directoryToCheck):
            processingResults.append(process_directory(directoryToCheck, photoDir))
    end = time.time()

    totalDirStats = merge_processingResults(processingResults)
    print_dirStats(totalDirStats)
    print ("Time taken: " + str(end - start))
        
if __name__ == "__main__":
    main()
