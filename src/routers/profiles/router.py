from fastapi import APIRouter, Query, HTTPException
from pydantic import UUID4

from .schemas import (
    GetProfileResponse, 
    GetProfileQueryField, 
    GetProfilesResponseProfile,
    GetProfilesResponse, 
    GetProfilesQuerySortBy, 
    GetProfilesQuerySortOrder,
    CreateProfileBody,
    CreateProfileResponse,
) 
from .service import (
    get_profile__get_profile,
    get_profiles__get_profiles,
    create_profile__create_profile,
)
from ...schemas import HTTPError
from ...database import ScientometricDatabase


router = APIRouter(prefix="/profiles")


@router.get("/{scientometric_database}/{profile_id}", response_model=GetProfileResponse | None)
async def get_profile(
        scientometric_database: ScientometricDatabase,
        profile_id: UUID4,
        fields: list[GetProfileQueryField] = Query(default=[]),
    ):
    res = await get_profile__get_profile(scientometric_database, profile_id)
    if res is None:
        return None
    
    return GetProfileResponse(
        full_name         = res.full_name,
        h_index           = res.h_index,
        url               = res.url,
        publication_count = res.publication_count if GetProfileQueryField.publication_count in fields else None,
        citation_count    = res.citation_count if GetProfileQueryField.citation_count in fields else None,
    )

@router.get("/{scientometric_database}", response_model=GetProfilesResponse)
async def get_profiles(
        scientometric_database: ScientometricDatabase,
        page: int = Query(default=1, ge=1, description="10 items per page"),
        sort_by: GetProfilesQuerySortBy = GetProfilesQuerySortBy.creation_date,
        sort_order: GetProfilesQuerySortOrder = GetProfilesQuerySortOrder.ascending,
    ):
    res = await get_profiles__get_profiles(
        scientometric_database=scientometric_database,
        page=page,
        results_per_page=10,
        sort_by=sort_by,
        sort_order=sort_order,
    )
    
    return GetProfilesResponse(
        profiles=[
            GetProfilesResponseProfile(
                profile_id = p.id,
                full_name  = p.full_name,
                h_index    = p.h_index,
                url        = p.url,
            )
            for p in res
        ]
    )

@router.post(
    "/{scientometric_database}", 
    response_model=CreateProfileResponse,
    responses={
        400: {
            "model": HTTPError,
            "description": "Profile already exists",
            "content": {
                "application/json": {
                    "example": { "detail": "Key {id} already exists" },
                },
            },
        },
    },
)
async def create_profile(
        scientometric_database: ScientometricDatabase,
        body: CreateProfileBody,
    ):
    try:
        profile = await create_profile__create_profile(scientometric_database, body)
    except RuntimeError as e:
        raise HTTPException(400, str(e)) from e
    
    return CreateProfileResponse(
        profile_id = profile.id,
    )
