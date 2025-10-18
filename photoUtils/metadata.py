import time
from datetime import datetime
import pyexiv2

PIXEL_HEIGHT_KEY = 'pixel_height'
PIXEL_WIDTH_KEY = 'pixel_width'

COMMON_ASPECT_RATIOS = {
    '1-1': 1.0,
    # landscape
    '4-3': 4/3,
    '5-4': 5/4,
    '7-5': 7/5,
    '3-2': 3/2,
    '16-9': 16/9,
    '16-10': 16/10,
    #portrait
    '3-4': 3/4,
    '4-5': 4/5,
    '5-7': 5/7,
    '2-3': 2/3,
    '9-16': 9/16,
    '10:16': 10/16,
    #panorama
    '1-2': 2,
    '1-3': 3,
    '1-4': 4,
    '1-5': 5,
}

# Threashold before a ratio is considered custom and not inside common ratio above
ASPECT_RATIO_THRESHOLD = 0.1

def get_metadata(filePath):
    image = pyexiv2.Image(filePath)
    rawExifData = image.read_exif()
    pixelHeight = image.get_pixel_height()
    pixelWidth = image.get_pixel_width()
    image.close()

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

    for ratioKey, ratioValue in COMMON_ASPECT_RATIOS.items():
        diff = abs(aspectRatio - ratioValue)
        if (diff < smallestDiff):
            smallestDiff = diff
            commonKey = ratioKey
    
    if (smallestDiff < ASPECT_RATIO_THRESHOLD):
        return commonKey
    
    return calculate_aspect_ratio(metadata[PIXEL_WIDTH_KEY], metadata[PIXEL_HEIGHT_KEY])

def get_created_time(metadata):
    metadataTimestamp = metadata['Image timestamp']
    return datetime.fromtimestamp(time.mktime(time.strptime(metadataTimestamp, "%Y:%m:%d %H:%M:%S")))
