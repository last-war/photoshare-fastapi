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
    """
    Unit Test Tags repository.
    """
    def setUp(self):
        """
        The setUp function is run before each test.
        It creates a mock session object, and a tag object with an id of 1, and the name &quot;test_tags&quot;.
        It also creates an image object with an id of 1, url &quot;url image&quot;, user_id of 1, and description
        &quot;test string description________________________________&quot;. The incoming data is set to &quot;#test_tags&quot;.

        Args:
            self: Represent the instance of the class

        Returns:
            A list of objects that will be used in the tests
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

        Args:
            self: Represent the instance of the object that is passed to the method when it is called

        Returns:
            A list of tags
        """
        expect_result = ["test_tags"]
        tags = parse_tags(self.incoming_data)
        self.assertEqual(tags, expect_result)
        self.assertListEqual(tags, expect_result)

    def test_parse_tags_not_found(self):
        """
        The test_parse_tags_not_found function tests the parse_tags function when there are no tags in the incoming data.
        The expected result is an empty list, and that is what we get.

        Args:
            self: Represent the instance of the class

        Returns:
            An empty list
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

        Args:
            self: Represent the instance of the object that is passed to the method when it is called

        Returns:
            The tag
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

        Args:
            self: Access the class attributes and methods

        Returns:
            The tag that it created
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
        The test_edit_tag_found function tests the edit_tag function.
            The test_edit_tag_found function is a coroutine that takes in self as an argument.
            The expect result variable is set to the tag variable, which was created earlier in this class.
            The edit tag name variable is set to &quot;edit name tag&quot;.  This will be used later on when we are editing our tags.
                We want to make sure that our tags can be edited properly and accurately, so we need a way of testing this out!
                That's what this test does for us!  It makes sure that our tags

        Args:
            self: Represent the instance of the class

        Returns:
            A result
        """
        expect_result = self.tag
        edit_tag_name = "edit_name_tag"
        tag_model = TagModel(tag_name=edit_tag_name)
        result = await edit_tag(expect_result, tag_model, db=self.session)
        self.assertEqual(result.tag_name, edit_tag_name)
        self.assertEqual(result.tag_name, expect_result.tag_name)
        self.assertEqual(result.id, expect_result.id)

    async def test_find_tag_by_id_found(self):
        """
        The test_find_tag_by_id_found function tests the find_tag function when a tag is found.
            The test_find_tag_by_id function sets up the following:
                - A mock session object with a query method that returns an object with a filter method that returns an object
                    with first and all methods. The first and all methods return None by default, but can be set to return
                    objects of any type. In this case, we set it to return our self.tag instance variable which is of type TagModel (see above).

        Args:
            self: Access the attributes and methods of the class in python

        Returns:
            The tag object and the name of that tag
        """
        expect_result = self.tag
        id_tag = self.tag.id
        self.session.query().filter().first.return_value = self.tag
        result = await find_tag(id_tag, db=self.session)
        self.assertEqual(result, expect_result)
        self.assertEqual(result.tag_name, expect_result.tag_name)

    async def test_find_tag_by_id_not_found(self):
        """
        The test_find_tag_by_id_not_found function tests the find_tag function when a tag is not found.
            The test_find_tag_by_id function creates a mock session and assigns it to self.session, then
            creates an expect result of None and assigns it to expect result, then sets the id of self.tag
            equal to id tag, then sets the return value for first() on filter() on query() on self.session
            equal to None (which simulates that no tags were found), finally calls find tag with id tag as its argument.

        Args:
            self: Represent the instance of the object that is passed to the method when it is called

        Returns:
            None
        """
        expect_result = None
        id_tag = self.tag.id
        self.session.query().filter().first.return_value = None
        result = await find_tag(id_tag, db=self.session)
        self.assertEqual(result, expect_result)
        self.assertIsNone(result)

    async def test_find_tag_found(self):
        """
        The test_find_tag_found function tests the find_tag function when a tag is found.
        It does this by creating a mock session and setting up the query to return an object.
        The test then calls find_tag with that tag name, and checks if it returns the expected result.

        Args:
            self: Represent the instance of the object that is passed to the method

        Returns:
            The tag that is passed into it
        """
        expect_result = self.tag
        tex_tag = self.tag.tag_name
        self.session.query().filter().first.return_value = self.tag
        result = await find_tag(tex_tag, db=self.session)
        self.assertEqual(result, expect_result)
        self.assertEqual(result.tag_name, expect_result.tag_name)

    async def test_find_tag_not_found(self):
        """
        The test_find_tag_not_found function tests the find_tag function when a tag is not found.
            The test_find_tag_not_found function uses the mock library to create a mock session object, and then sets up
            that object's query method to return another mocked object. This second mocked object has its filter method set
            up to return yet another mocked object, which in turn has its first method set up so that it returns None. This
            simulates what happens when no tag with the given name exists in the database: The query() call returns an empty list,
            and calling first on an

        Args:
            self: Represent the instance of the object that is passed to the method

        Returns:
            None
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
        The test_delete_tag_found function is a coroutine, so it must be called with 'await' and runs asynchronously.
        The test_delete_tag found function takes no arguments, but uses self to access class variables that are set up in
        the setUpClass method at the top of this TestCase class definition.

        Args:
            self: Represent the instance of the class

        Returns:
            The tag that was deleted
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
        The test case for this function is when a tag does not exist in the database, so it should return None.

        Args:
            self: Access the attributes and methods of the class in python

        Returns:
            None
        """
        expect_result = None
        tex_tag = self.tag.tag_name
        self.session.query().filter().first.return_value = None
        result = await delete_tag(tex_tag, db=self.session)
        self.assertEqual(result, expect_result)
        self.assertIsNone(result)

    async def test_get_images_by_tag_found(self):
        """
        The test_get_images_by_tag_found function tests the get_images_by_tag function in the image.py file.
        The test is successful if it returns a list of images that have been tagged with a specific tag.

        Args:
            self: Represent the instance of the class

        Returns:
            The list of images that match the tag
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

        Args:
            self: Access the attributes and methods of the class in python

        Returns:
            None
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
