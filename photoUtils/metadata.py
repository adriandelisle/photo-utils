import time
from enum import StrEnum
from datetime import datetime
import pyexiv2

PIXEL_HEIGHT_KEY = 'pixel_height'
PIXEL_WIDTH_KEY = 'pixel_width'

class AspectTypes(StrEnum):
    Sqaure = 'square'
    Landscape = 'landscape'
    Portrait = 'portrait'
    Panorama = 'panorama'
    Custom = 'custom'

COMMON_ASPECT_RATIOS = {
    '1-1': {
        "label": "1-1",
        "value": 1.0,
        "type": AspectTypes.Sqaure,
    },
    # landscape
    '4-3': {
        "label": "4-3",
        "value": 4/3,
        "type": AspectTypes.Landscape
    },
    '5-4': {
        "label": "5-4",
        "value": 5/4,
        "type": AspectTypes.Landscape
    },
    '7-5': {
        "label": "7-5",
        "value": 7/5,
        "type": AspectTypes.Landscape
    },
    '3-2': {
        "label": "3-2",
        "value": 3/2,
        "type": AspectTypes.Landscape
    },
    '16-9': {
        "label": "16-9",
        "value": 16/9,
        "type": AspectTypes.Landscape
    },
    '16-10': {
        "label": "16-10",
        "value": 16/10,
        "type": AspectTypes.Landscape
    },
    #portrait
    '3-4': {
        "label": '3-4',
        "value": 3/4,
        "type": AspectTypes.Portrait
    },
    '4-5': {
        "label": '4-5',
        "value": 4/5,
        "type": AspectTypes.Portrait
    },
    '5-7': {
        "label": '5-7',
        "value": 5/7,
        "type": AspectTypes.Portrait
    },
    '2-3': {
        "label": '2-3',
        "value": 2/3,
        "type": AspectTypes.Portrait
    },
    '9-16': {
        "label": '9-16',
        "value": 9/16,
        "type": AspectTypes.Portrait
    },
    '10-16': {
        "label": '10-16',
        "value": 10/16,
        "type": AspectTypes.Portrait
    },
    #panorama
    '1-2': {
        "label": '1-2',
        "value": 1/2,
        "type": AspectTypes.Panorama
    },
    '1-3': {
        "label": '1-3',
        "value": 1/3,
        "type": AspectTypes.Panorama
    },
    '1-4': {
        "label": '1-4',
        "value": 1/4,
        "type": AspectTypes.Panorama
    },
    '1-5': {
        "label": '1-5',
        "value": 1/5,
        "type": AspectTypes.Panorama
    },
    '1-8': {
        "label": '1-8',
        "value": 1/8,
        "type": AspectTypes.Panorama
    },
}

# Threashold before a ratio is considered custom and not inside common ratio above
ASPECT_RATIO_THRESHOLD = 0.1

def get_metadata(filePath):
    # open the file manual since windows does some funky stuff with encoding
    # https://github.com/LeoHsiao1/pyexiv2/issues/131
    # https://github.com/LeoHsiao1/pyexiv2/blob/master/docs/Tutorial.md#class-imagedata
    # Aéxətəm Regional Park (Colony Farm) was causing some issues
    with open(filePath, 'rb') as file:
        with pyexiv2.ImageData(file.read()) as image:
            rawExifData = image.read_exif()
            pixelHeight = image.get_pixel_height()
            pixelWidth = image.get_pixel_width()

    # Extract exif data
    metadata = {}
    for field in rawExifData:
        keyValue = field.split(':')
        if len(keyValue) >= 2:
            metadata[keyValue[0].strip()] = ":".join(keyValue[1:]).strip()
    metadata[PIXEL_HEIGHT_KEY] = pixelHeight
    metadata[PIXEL_WIDTH_KEY] = pixelWidth
    return metadata

def calculate_aspect_ratio(width: int, height: int) -> str:
    def gcd(a, b):
        return a if b == 0 else gcd(b, a % b)

    r = gcd(width, height)
    x = int(width / r)
    y = int(height / r)

    return f"{x}-{y}"

def get_aspect_ratio(metadata) -> str:
    height = metadata[PIXEL_HEIGHT_KEY]
    width = metadata[PIXEL_WIDTH_KEY]
    
    return float("{:.2f}".format(width / height))

def get_nearest_common_aspect_ratio(metadata) -> str:
    aspectRatio = get_aspect_ratio(metadata)
    (commonKey, smallestDiff) = ('none', float('inf'))

    for ratioKey, ratioInfo in COMMON_ASPECT_RATIOS.items():
        diff = abs(aspectRatio - ratioInfo["value"])
        if (diff < smallestDiff):
            smallestDiff = diff
            commonKey = ratioKey
    
    if (smallestDiff < ASPECT_RATIO_THRESHOLD):
        return COMMON_ASPECT_RATIOS[commonKey]
    
    customAspectRatio = calculate_aspect_ratio(metadata[PIXEL_WIDTH_KEY], metadata[PIXEL_HEIGHT_KEY])
    return {
        "type": AspectTypes.Custom,
        "label": customAspectRatio
    }

def get_created_time(metadata):
    metadataTimestamp = metadata['Image timestamp']
    return datetime.fromtimestamp(time.mktime(time.strptime(metadataTimestamp, "%Y:%m:%d %H:%M:%S")))
