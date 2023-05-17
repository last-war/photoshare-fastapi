from typing import List

from src.database.models import Image


def create_transformation_tags(tags: List[Image]):
    tags_in_text = f"#"
    for tag in tags:
        tags_in_text += tag.tag_name

    return tags_in_text
