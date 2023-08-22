from pydantic import BaseModel
from typing import List, Optional, Union


class Publication(BaseModel):
    title: str
    venue: str
    url: str
    authors: Union[str, List[str]]
    num_citations: int
    pub_year: Optional[int]
