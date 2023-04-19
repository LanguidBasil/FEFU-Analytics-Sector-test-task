from sqlalchemy.exc import IntegrityError
from sqlalchemy import select, Column

from .schemas import (
    GetProfilesQuerySortBy,
    GetProfilesQuerySortOrder,
    CreateProfileBody,
) 
from ...database import session_maker, Profile, ScientometricDatabase


async def get_profile__get_profile(
        scientometric_database: ScientometricDatabase,
        profile_id: str, 
    ) -> Profile | None:
    
    async with session_maker() as session:
        res = (await session.execute(
            select(Profile).
            where(Profile.scientometric_database == scientometric_database).
            where(Profile.id == profile_id)
        )).scalar()
        return res
    
    
async def get_profiles__get_profiles(
        scientometric_database: ScientometricDatabase,
        page: int,
        results_per_page: int,
        sort_by: GetProfilesQuerySortBy,
        sort_order: GetProfilesQuerySortOrder,
    ) -> list[Profile]:
    
    sort_mapping: dict[GetProfilesQuerySortBy, Column] = {
        GetProfilesQuerySortBy.creation_date: Profile.creation_date,
        GetProfilesQuerySortBy.h_index: Profile.h_index,
    }
    column_to_sort_by = sort_mapping[sort_by]
    
    if sort_order == GetProfilesQuerySortOrder.descending:
        column_to_sort_by = column_to_sort_by.desc()
    
    
    async with session_maker() as session:
        offset = (page - 1) * results_per_page
        profiles_scalar_result = (await session.execute(
            select(Profile).
            where(Profile.scientometric_database == scientometric_database).
            offset(offset).
            limit(results_per_page).
            order_by(column_to_sort_by)
        )).scalars()
        
        return list(profiles_scalar_result)


async def create_profile__create_profile(
        scientometric_database: ScientometricDatabase,
        body: CreateProfileBody,
    ) -> Profile:
    
    try:
        p = Profile(
            id = body.profile_id,
            full_name = body.full_name,
            scientometric_database = scientometric_database,
            publication_count = body.publication_count,
            citation_count = body.citation_count,
            h_index = body.h_index,
            url = body.url,
        )
        
        async with session_maker() as session:
            session.add(p)
            await session.commit()
        
        return p
    except IntegrityError as e:
        raise RuntimeError(f"Key {p.id} already exists") from e
