""" Global config for file manager """

# internal modules
import os


ALLOWED_EXTENSIONS = set(['txt', 'pdf', 'png', 'jpg', 'jpeg', 'gif'])
UPLOAD_FOLDER = 'store'

if not os.path.exists(UPLOAD_FOLDER):
    os.makedir(UPLOAD_FOLDER)
