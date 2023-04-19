from pydantic import BaseModel, conint, confloat

from ...database import ScientometricDatabase


class PublicationActivityItem(BaseModel):
    total_publication_count: conint(ge=0)
    total_citation_count: conint(ge=0)
    average_h_index: confloat(ge=0)

class PublicationActivityResponse(BaseModel):
    items: dict[ScientometricDatabase, PublicationActivityItem]
