from datetime import datetime
from typing import Optional, List

class ImageModel(BaseModel):
    description: str = Field('description', min_length=20, max_length=255)

