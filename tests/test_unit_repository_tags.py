import unittest
from unittest.mock import MagicMock, patch
from sqlalchemy.orm import Session

from src.schemas.tags import TagModel
from src.database.models import Tag, tag_to_image, Image
from src.repository.tags import (
    parse_tags,
    create_tags,
    edit_tag,
    find_tag,
    delete_tag,
    get_images_by_tag
)


"""
Unit test repository tags.
"""


class TestTags(unittest.IsolatedAsyncioTestCase):
    def setUp(self):
        """
        The setUp function is run before each test.
        It creates a mock session object, and a tag object with an id of 1, and the name &quot;test_tags&quot;.
        It also creates an image object with an id of 1, url &quot;url image&quot;, user_id of 1, and description
        &quot;test string description________________________________&quot;. The incoming data is set to &quot;#test_tags&quot;.

        :param self: Represent the instance of the class
        :return: A dictionary of objects that will be used in the tests
        """
        self.session = MagicMock(spec=Session)
        self.tag = Tag(id=1, tag_name="test_tags")
        self.incoming_data = "#test_tags"
        self.image = Image(
            id=1,
            image_url="url image",
            user_id=1,
            description="test string description________________________________",
        )

    def test_parse_tags_found(self):
        """
        The test_parse_tags_found function tests the parse_tags function.
        It checks to see if the tags are found in the incoming data and returns a list of those tags.

        :param self: Represent the instance of the class
        :return: A list of tags
        """
        expect_result = ["test_tags"]
        tags = parse_tags(self.incoming_data)
        self.assertEqual(tags, expect_result)
        self.assertListEqual(tags, expect_result)

    def test_parse_tags_not_found(self):
        """
        The test_parse_tags_not_found function tests the parse_tags function when there are no tags in the incoming data.
        The expected result is an empty list, and that is what we get.

        :param self: Represent the instance of the object that is passed implicitly into the method
        :return: An empty list
        """
        expect_result = list()
        incoming_data = ""
        tags = parse_tags(incoming_data)
        self.assertEqual(tags, expect_result)
        self.assertListEqual(tags, expect_result)

    async def test_create_new_tags_existing_tag(self):
        """
        The test_create_new_tags_existing_tag function tests the create_tags function when a tag already exists in the database.
        The test creates an incoming data list with one tag, and then sets up a mock session object that returns that same tag when queried.
        The test then calls the create_tags function with this incoming data and mock session object, and asserts that it returns a list containing only one element:
        the original inputted Tag object.

        :param self: Represent the instance of the class
        :return: The tag
        """
        expect_result = [self.tag]
        self.session.query().filter().first.return_value = self.tag
        result = await create_tags(self.incoming_data, db=self.session)
        self.assertEqual(result, expect_result)
        self.assertEqual(result[0], expect_result[0])

    async def test_create_new_tags_new_tag(self):
        """
        The test_create_new_tags_new_tag function tests the create_tags function when a new tag is created.
        The test_create_new_tags_new_tag function uses patch to mock the Tag class and return a MagicMock object.
        The test then calls the create tags function with incoming data that does not exist in the database,
        and asserts that it returns an array containing one element, which is equal to self.tag.

        :param self: Represent the instance of the class
        :return: A list of tags
        """
        expect_result = [self.tag]
        self.session.query().filter().first.return_value = None
        self.session.add.return_value = MagicMock(return_value=self.tag)
        with patch('src.repository.tags.Tag', return_value=self.tag):
            result = await create_tags(self.incoming_data, db=self.session)
        self.assertEqual(result, expect_result)
        self.assertEqual(result[0], expect_result[0])

    async def test_edit_tag_found(self):
        """
        The test_edit_tag_found function tests the edit_tag function in the tag.py file.
        The test_edit_tag_found function is a coroutine that takes no arguments and returns nothing.
        The test case for this function is when a user wants to edit an existing tag, but they do not know its id number.

        :param self: Represent the instance of the class
        :return: The tag object
        """
        expect_result = self.tag
        tag_model = TagModel(tag_name=self.tag.tag_name)
        self.session.query().filter().first.return_value = self.tag
        result = await edit_tag(tag_model, db=self.session)
        self.assertEqual(result, expect_result)
        self.assertEqual(result.tag_name, expect_result.tag_name)

    async def test_edit_tag_not_found(self):
        """
        The test_edit_tag_not_found function tests the edit_tag function when it is unable to find a tag in the database.
        The test_edit_tag_not_found function uses a mock session object and returns None if no tag is found.

        :param self: Represent the instance of the class
        :return: None
        """
        expect_result = None
        tag_model = TagModel(tag_name=self.tag.tag_name)
        self.session.query().filter().first.return_value = None
        result = await edit_tag(tag_model, db=self.session)
        self.assertEqual(result, expect_result)
        self.assertIsNone(result)

    async def test_find_tag_found(self):
        """
        The test_find_tag_found function tests the find_tag function.
            The test_find_tag_found function is a coroutine that takes no arguments.
            The test uses the pytest-asyncio library to run asynchronous code in a synchronous manner.

        :param self: Represent the instance of the class
        :return: The tag that was found
        """
        expect_result = self.tag
        tex_tag = self.tag.tag_name
        self.session.query().filter().first.return_value = self.tag
        result = await find_tag(tex_tag, db=self.session)
        self.assertEqual(result, expect_result)
        self.assertEqual(result.tag_name, expect_result.tag_name)

    async def test_find_tag_not_found(self):
        """
        The test_find_tag_not_found function tests the find_tag function when it does not find a tag.
            It creates a mock session and adds an expected result to the mock session's query().filter().first() method.
            The test then calls the find_tag function with a tag name that is not in the database, and checks that it returns None.

        :param self: Access the instance attributes and methods
        :return: None
        """
        expect_result = None
        tex_tag = self.tag.tag_name
        self.session.query().filter().first.return_value = None
        result = await find_tag(tex_tag, db=self.session)
        self.assertEqual(result, expect_result)
        self.assertIsNone(result)

    async def test_delete_tag_found(self):
        """
        The test_delete_tag_found function tests the delete_tag function in the tags.py file.
        The test_delete_tag_found function is a coroutine that takes no arguments and returns nothing.
        The test uses a mock session object to simulate database interactions, and it also uses
        a mock tag object to simulate an actual tag from the database.

        :param self: Represent the instance of the object that is passed to the method
        :return: The tag object
        """
        expect_result = self.tag
        tex_tag = self.tag.tag_name
        self.session.query().filter().first.return_value = self.tag
        result = await delete_tag(tex_tag, db=self.session)
        self.assertEqual(result, expect_result)
        self.assertEqual(result.tag_name, expect_result.tag_name)

    async def test_delete_tag_not_found(self):
        """
        The test_delete_tag_not_found function tests the delete_tag function in the tags.py file.
        The test_delete_tag_not_found function is a coroutine that takes no arguments and returns nothing.
        The test case for this function is when we try to delete a tag that does not exist in our database.

        :param self: Represent the instance of the class
        :return: None
        """
        expect_result = None
        tex_tag = self.tag.tag_name
        self.session.query().filter().first.return_value = None
        result = await delete_tag(tex_tag, db=self.session)
        self.assertEqual(result, expect_result)
        self.assertIsNone(result)

    async def test_get_images_by_tag_found(self):
        """
        The test_get_images_by_tag_found function tests the get_images_by_tag function.
        The test is successful if the result of calling get_images_by_tag with a tag name, limit, and offset matches an expected result.

        :param self: Represent the instance of the class
        :return: A list of images with the specified tag
        """
        expect_result = [self.image]
        tex_tag = self.tag.tag_name
        tag_limit = 10
        tag_offset = 0
        self.session.query().join().join().filter().order_by().limit().offset().all.return_value = [self.image]
        result = await get_images_by_tag(tag=tex_tag, limit=tag_limit, offset=tag_offset, db=self.session)
        self.assertEqual(result, expect_result)
        self.assertEqual(result[0].id, expect_result[0].id)
        self.assertEqual(result[0].image_url, expect_result[0].image_url)
        self.assertEqual(result[0].description, expect_result[0].description)
        self.assertEqual(result[0].user_id, expect_result[0].user_id)

    async def test_get_images_by_tag_not_found(self):
        """
        The test_get_images_by_tag_not_found function tests the get_images_by_tag function in the image.py file
        to ensure that it returns None when no images are found with a given tag.

        :param self: Access the attributes and methods of the class in python
        :return: None
        """
        expect_result = None
        tex_tag = self.tag.tag_name
        tag_limit = 10
        tag_offset = 0
        self.session.query().join().join().filter().order_by().limit().offset().all.return_value = None
        result = await get_images_by_tag(tag=tex_tag, limit=tag_limit, offset=tag_offset, db=self.session)
        self.assertEqual(result, expect_result)
        self.assertIsNone(result)


if __name__ == '__main__':
    unittest.main()
