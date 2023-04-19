from enum import Enum
from pydantic import BaseModel, UUID4, constr, conint, AnyHttpUrl


class ExceptionModel(BaseModel):
    message: str


class GetProfileQueryField(str, Enum):
    publication_count = "publication_count"
    citation_count = "citation_count"

class GetProfileResponse(BaseModel):
    full_name: constr(strip_whitespace=True)
    h_index: conint(ge=0)
    url: AnyHttpUrl
    publication_count: conint(ge=0) | None = None
    citation_count: conint(ge=0) | None = None
    

class GetProfilesQuerySortBy(str, Enum):
    creation_date = "creation_date"
    h_index = "h_index"
    
class GetProfilesQuerySortOrder(str, Enum):
    ascending = "ascending"
    descending = "descending"

class GetProfilesResponseProfile(BaseModel):
    profile_id: UUID4
    full_name: constr(strip_whitespace=True)
    h_index: conint(ge=0)
    url: AnyHttpUrl

class GetProfilesResponse(BaseModel):
    profiles: list[GetProfilesResponseProfile]


class CreateProfileBody(BaseModel):
    profile_id: UUID4
    full_name: constr(strip_whitespace=True)
    publication_count: conint(ge=0)
    citation_count: conint(ge=0)
    h_index: conint(ge=0)
    url: AnyHttpUrl

class CreateProfileResponse(BaseModel):
    profile_id: UUID4
