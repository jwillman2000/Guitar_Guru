from app.schemas.exercise import CamelModel


class TagOut(CamelModel):
    id: int
    category: str
    name: str
    slug: str
