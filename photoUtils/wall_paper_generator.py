import os
import subprocess

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
    print (imageSize)
    return "{:.2f}".format(imageSize[0] / imageSize[1])

##metadata = get_metadata(r'P:\Pictures\Python Test\Timelapses\Abbotsford Tulip Festival 09-04-2016\Edits\Output\No watermark\DSC_0062.jpg')
##print (get_aspect_ratio(metadata))

aspectRatios = {}
for directoryToCheck in directories:
    for dir in os.listdir(directoryToCheck):
        print (dir)
        for dirPath, dirs, files in os.walk(os.path.join(directoryToCheck, dir)):
            if len(files) <= 0:
                continue

            print (dirPath)
            if dirPath.lower().find("no watermark") != -1:
                for file in files:
                    if is_picture(file):
                        filePath = os.path.join(dirPath, file)
                        metadata = get_metadata(filePath)
                        aspectRatio = get_aspect_ratio(metadata)
                        print (aspectRatio)
                        if aspectRatio in aspectRatios:
                            aspectRatios[aspectRatio].append(filePath)
                        else:
                            aspectRatios[aspectRatio] = [filePath]
##                        print (filePath)
##                        print (get_metadata(filePath))
print (aspectRatios)
for aspectRatio, photos in aspectRatios.items():
    print (aspectRatio, len(photos))
    

