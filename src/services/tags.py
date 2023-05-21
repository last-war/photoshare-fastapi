from typing import List

from src.database.models import Tag


def create_transformation_tags(tags: List[Tag]) -> str:
    """
    create tag for transformation operations

    Arguments:
        tags (List[Tag]): list tag objects for write tag strings

    Returns:
        List[Tag]: tag strings for new image
    """
    tags_in_text = f"#"
    for tag in tags:
        tags_in_text += tag.tag_name

    return tags_in_text
