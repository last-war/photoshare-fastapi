import unittest

from src.database.models import Tag
from src.services.tags import (
    create_transformation_tags
)


"""
Unit test services tags.
"""


class TestTags(unittest.IsolatedAsyncioTestCase):
    """
    Unit test services tags.
    """
    def setUp(self):
        """
        The setUp function is run before each test.
        It creates a Tag object and stores it in the self.tag_2 variable, which can be accessed by any of the tests in this class.

        Args:
            self: Represent the instance of the class

        Returns:
            The self
        """
        self.tag_1 = Tag(id=1, tag_name="tag_1#Test#Test2")
        self.tags = [self.tag_1]

    def test_create_transformation_tags(self):
        """
        The test_create_transformation_tags function tests the create_transformation_tags function.
        It does this by creating a list of tags, and then passing that list to the create_transformation_tags function.
        The expected result is a string with all of the tags in it, separated by #tag#'s. The actual result is compared to
        the expected result using an assert statement.

        Args:
            self: Represent the instance of the class

        Returns:
            A string of tags with the
        """
        expected_result = "#tag_1#Test#Test2"
        result = create_transformation_tags(self.tags)
        self.assertEqual(result, expected_result)


if __name__ == '__main__':
    unittest.main()
