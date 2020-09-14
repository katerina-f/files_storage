""" Executable module of file manager """

# internal modules
import os

# external modules
from flask import Flask, request, send_from_directory
from flask_restful import Api, Resource

from hashlib import md5
from werkzeug.utils import secure_filename

#project modules
from config import ALLOWED_EXTENSIONS, UPLOAD_FOLDER


app = Flask(__name__)
api = Api(app)

client = app.test_client()


def allowed_file(filename):
    """ Check file extension is allowed """

    return "." in filename and \
           filename.rsplit(".", 1)[1] in ALLOWED_EXTENSIONS


class FileManager(Resource):

    """
    Class for work with files.
    Supports GET, POST, DELETE options
    """

    def get(self, hash_data=None, download=None):
        if not hash_data or len(hash_data) < 2:
            return ("Valid hash parameter is needed"), 404

        hash_dir = hash_data[0:2]
        download_dir = UPLOAD_FOLDER + "/" + hash_dir

        if os.path.isfile(download_dir+ "/"+ hash_data):
            if download:
                return send_from_directory(download_dir, hash_data, as_attachment=True)
            else:
                return ("File exists"), 200
        else:
            return ("File was not found"), 404

    def delete(self, hash_data):
        hash_dir = hash_data[0:2]
        download_dir = UPLOAD_FOLDER + "/" + hash_dir + "/" + hash_data

        if os.path.isfile(download_dir):
            os.remove(download_dir)
            return 204
        else:
            return ("File was not found"), 404

    def post(self):
        if "file" not in request.files:
            return ("File is needed"), 400

        file_ = request.files.get("file")
        if not allowed_file(file_.filename):
            return ("Not allowed filename!"), 403

        filename = secure_filename(file_.filename)
        new_hash = md5(filename.encode()).hexdigest()
        hash_dir = new_hash[0:2]
        upload_dir = UPLOAD_FOLDER + "/" + hash_dir
        try:
            os.mkdir(upload_dir)
            file_.save(os.path.join(upload_dir, new_hash))
        except FileExistsError:
            file_.save(os.path.join(upload_dir, new_hash))
        finally:
            return new_hash, 201

api.add_resource(FileManager, "/file_manager", "/file_manager/<hash_data>",
                               "/file_manager/<hash_data>/<download>")

if __name__ == "__main__":
    app.run(debug=True, host="0.0.0.0")
