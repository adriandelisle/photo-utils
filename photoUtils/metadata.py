import subprocess
from pkg_resources import resource_filename

exiv2Path = resource_filename(__name__, 'exiv2-0.25-win/exiv2.exe')

def get_metadata(filePath):
    ## http://stackoverflow.com/a/7006424
    CREATE_NO_WINDOW = 0x08000000
    DETACHED_PROCESS = 0x00000008
    processResult = subprocess.run(
        args = [exiv2Path, filePath],
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
