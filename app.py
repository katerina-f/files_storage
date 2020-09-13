""" Executable module of file manager """

# internal modules
import os

# external modules
from flask import Flask, jsonify, request, redirect, url_for, send_file
from flask_restful import Api, Resource, reqparse

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


class FileGet(Resource):

    """
    Class for work with files.
    Supports GET option
    """

    def get(self, hash_data=None):
        if not hash_data:
            return '''
                <!doctype html>
                <title>Upload new File</title>
                <h1>Upload new File</h1>
                <form action='' method=post enctype=multipart/form-data>
                  <p><input type=file name=file>
                     <input type=submit value=Upload>
                </form>
                '''
        if len(hash_data) < 2:
            return ("Valid hash parameter is needed"), 404

        hash_dir = hash_data[0:2]
        download_dir = UPLOAD_FOLDER + "/" + hash_dir + "/" + hash_data

        if os.path.isfile(download_dir):
            return send_file(download_dir,  as_attachment=True), 200
        else:
            return ("File was not found"), 404


class FileDelete(Resource):
    """

    Class for work with files.
    Supports DELETE option

    """

    def get(self, hash_data=None):
        return '''
                <!doctype html>
                <title>Upload new File</title>
                <h1>Upload new File</h1>
                <form action='' method=delete enctype=multipart/form-data>
                  <p><input type=file name=file>
                     <input type=submit value=Upload>
                </form>
                '''

    def delete(self, hash_data):
        hash_dir = hash_data[0:2]
        download_dir = UPLOAD_FOLDER + "/" + hash_dir + "/" + hash_data

        if os.path.isfile(download_dir):
            os.remove(download_dir)
            return ("File was successfully deleted"), 204
        else:
            return ("File was not found"), 404


class FileUpload(Resource):
    """

    Class for work with files.
    Supports POST option

    """
    def get(self, hash_data=None):
        return '''
            <!doctype html>
            <title>Upload new File</title>
            <h1>Upload new File</h1>
            <form action='' method=post enctype=multipart/form-data>
                <p><input type=file name=file>
                    <input type=submit value=Upload>
            </form>
            '''

    def post(self):
        if "file" not in request.files:
            return ("File is needed"), 403

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


api.add_resource(FileGet, "/get_file", "/get_file/<hash_data>")
api.add_resource(FileDelete, "/delete", "/delete/<hash_data>")
api.add_resource(FileUpload, "/upload", "/upload/<hash_data>")


if __name__ == "__main__":
    app.run(debug=True)
