from pydantic import BaseModel
from typing import List, Optional, Union


class Recommendation(BaseModel):
    class_topic: str
    title: str
    venue: str
    authors: Union[str, List[str]]
    url: str
    pub_year: Optional[int]
