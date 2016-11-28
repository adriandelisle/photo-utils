def is_picture(fileName):
    acceptedFileTypes = ['.jpg', '.nef']
    for fileType in acceptedFileTypes:
        if fileName.lower().endswith(fileType):
            return True
    return False
