import hashlib
import re
from uuid import uuid4

import cloudinary
import cloudinary.uploader
from cloudinary import api
from fastapi import HTTPException
from starlette import status

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
        The upload function takes a file and uploads it to the cloudinary server.
            The public_id is the name of the file on cloudinary, and overwrite=True means that if there is already a file with that name, it will be overwritten.

        :param file: Specify the file to be uploaded
        :param public_id: str: Specify the public id of the image
        :param overwrite: Determine whether the image should be overwritten if it already exists
        :return: A dictionary with the following keys:
        :doc-author: Trelent
        """
        r = cloudinary.uploader.upload(file, public_id=public_id, overwrite=overwrite)
        return r
    
    @staticmethod
    def get_url_for_avatar(public_id, r):
        """
        The get_url_for_avatar function takes in a public_id and an r
        (which is the result of a cloudinary.api.resource call)
        and returns the URL for that avatar image, which will be used to display it on the page.

        :param public_id: Identify the image in cloudinary
        :param r: Get the version of the image
        :return: A url
        :doc-author: Trelent
        """
        src_url = cloudinary.CloudinaryImage(public_id) \
            .build_url(width=250, height=250, crop='fill', version=r.get('version'))
        return src_url
    
    @staticmethod
    def get_url_for_image(file_name):
        """
        The get_url_for_image function takes a file name as an argument and returns the url for that image.
        The function uses the cloudinary library to generate a url from the file name.

        :param file_name: Specify the name of the file that is to be uploaded
        :return: The url for the image
        :doc-author: Trelent
        """
        src_url = cloudinary.utils.cloudinary_url(file_name)
        return src_url[0]

    @staticmethod
    def get_transformation_image(public_id: str, transformation: str):
        """
        The get_transformation_image function takes in a public_id and transformation string,
            then returns the url of the transformed image. If no transformation is found, it returns None.

        :param public_id: str: Get the public id of the image
        :param transformation: str: Get the transformation name from the transformation class
        :return: The url of the transformed image
        :doc-author: Trelent
        """
        public_id = re.search(r'(?<=/v\d/).+', public_id).group(0)
        if transformation in Transformation.name.keys():
            transformation_image_url = cloudinary.utils.cloudinary_url(public_id,
                                                                       transformation=[Transformation.name.get(transformation)])[0]
            return transformation_image_url

        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Not Found")


class Standart:
    name = "standart"
    transformation = {"width": 500, "height": 500, "gravity": "faces", "crop": "fill"}


class Radius:
    name = "radius"
    transformation = {"radius": "max", "width": 500, "height": 500, "gravity": "faces", "crop": "fill"}


class Grayscale:
    name = "grayscale"
    transformation = {"effect": "grayscale", "width": 500, "height": 500, "gravity": "faces", "crop": "fill"}


class Cartoonify:
    name = "cartoonify"
    transformation = {"effect": "cartoonify", "width": 500, "height": 500, "gravity": "faces", "crop": "fill"}


class Vectorize:
    name = "vectorize"
    transformation = {"effect": "vectorize:colors:2:detail:0.05", "width": 500, "height": 500, "gravity": "faces", "crop": "fill"}


class Transformation:
    name = {
        "grayscale": Grayscale.transformation,
        "cartoonify": Cartoonify.transformation,
        "radius": Radius.transformation,
        "standart": Standart.transformation,
        "vectorize": Vectorize.transformation
    }
