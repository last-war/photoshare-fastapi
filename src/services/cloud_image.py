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
    def generate_name_avatar(email: str):
        """
        The generate_name_avatar function takes an email address as input and returns a unique avatar name.
        The function uses the first 12 characters of the SHA256 hash of the email address to generate a unique string.
        This string is then appended with &quot;web9/&quot; to create a valid S3 bucket key.

        :param email: str: Specify the type of parameter that is expected to be passed into the function
        :return: A string that is a combination of the prefix &quot;web9/&quot;
        and a 12-character hash of the email address
        :doc-author: Trelent
        """
        name = hashlib.sha256(email.encode('utf-8')).hexdigest()[:12]
        return f"web9/{name}"

    @staticmethod
    def upload(file, public_id: str, overwrite=True):
        """
        The upload function takes a file and public_id as arguments.
        The function then uploads the file to Cloudinary using the public_id provided.
        If no public_id is provided, one will be generated automatically.

        :param file: Specify the file to be uploaded
        :param public_id: str: Set the public id of the image
        :return: A dictionary with the following keys:
        :doc-author: Trelent
        """
        r = cloudinary.uploader.upload(file, public_id=public_id, overwrite=overwrite)
        return r

    @staticmethod
    def get_url_for_image(file_name):
        src_url = cloudinary.utils.cloudinary_url(file_name)
        return src_url[0]
