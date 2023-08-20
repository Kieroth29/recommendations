from pydantic import BaseModel
from typing import List, Union


class Recommendation(BaseModel):
    title: str
    venue: str
    authors: Union[str, List[str]]
    url: str
    pub_year: int
