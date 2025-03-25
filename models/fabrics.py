from pydantic import BaseModel


class Fabrics(BaseModel):
    """
    Represents the data structure of a Fabric.
    """

    name: str
    supplier: str
    categories: str
    capacity: str
    composition: str
    paper_weight: str
    description: str


class FabricImages(BaseModel):
    """
    Represents the data structure of a Fabric Image.
    """

    name: str
    location: str
    price: str
    capacity: str
    rating: float
    reviews: int
    description: str


class FabricLinks(BaseModel):
    """
    Represents the data structure of a Fabric Image.
    """

    name: str
    url: str

