import hashlib
from uuid import uuid4

import cloudinary
import cloudinary.uploader

from src.conf.config import settings


"""
Photo storage service.
"""


class CloudImage:
    """
    Class Photo storage.
    """
    cloudinary.config(
        cloud_name=settings.cloudinary_name,
        api_key=settings.cloudinary_api_key,
        api_secret=settings.cloudinary_api_secret,
        secure=True
    )

    @staticmethod
    def generate_name_image():
        """
        The generate_name_image function generates a unique name for the image file.
        It uses the uuid4 function to generate a random UUID, and then hashes it using SHA256.
        The resulting hash is converted to hexadecimal format, and returned as a string.

        :return: A string of the form &quot;photoshare/&lt;sha256 hash&gt;&quot;
        :doc-author: Trelent
        """
        name = hashlib.sha256(str(uuid4()).encode('utf-8')).hexdigest()
        return f"photoshare/{name}"

    @staticmethod
    def upload(file, file_name: str):
        """
        The upload function takes a file and public_id as arguments.
        The function then uploads the file to Cloudinary using the public_id provided.
        If no public_id is provided, one will be generated automatically.

        :param file: Upload a file to the cloudinary server
        :param file_name: str: Set the public id of the image
        :return: A dictionary of data about the uploaded image
        :doc-author: Trelent
        """
        r = cloudinary.uploader.upload(file, public_id=file_name)
        return r

    @staticmethod
    def get_url_for_image(file_name):
        src_url = cloudinary.utils.cloudinary_url(file_name)
        return src_url[0]
