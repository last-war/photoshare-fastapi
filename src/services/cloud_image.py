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
    def upload(file, public_id: str):
        """
        The upload function takes a file and public_id as arguments.
        The function then uploads the file to Cloudinary using the public_id provided.
        If no public_id is provided, one will be generated automatically.

        :param file: Upload a file to the cloudinary server
        :param public_id: str: Set the public id of the image
        :return: A dictionary of data about the uploaded image
        :doc-author: Trelent
        """
        r = cloudinary.uploader.upload(file, public_id=public_id, overwrite=True)
        return r

    @staticmethod
    def get_url_for_image(public_id, r):
        """
        The get_url_for_avatar function takes in a public_id and an r (which is the result of a cloudinary.api.resource call)
        and returns the URL for that avatar image, which will be used to display it on the page.

        :param public_id: Identify the image in cloudinary
        :param r: Get the version of the image
        :return: The url of the avatar image
        :doc-author: Trelent
        """
        src_url = cloudinary.CloudinaryImage(public_id) \
            .build_url(width=250, height=250, crop='fill', version=r.get('version'))
        return src_url
