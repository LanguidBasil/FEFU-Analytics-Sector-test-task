from sqlalchemy import select, func

from .schemas import PublicationActivityResponse, PublicationActivityItem
from ...database import Profile, session_maker


async def publication_activity__calculate() -> PublicationActivityResponse:
    
    async with session_maker() as session:
        res = (await session.execute(
            select(
                Profile.scientometric_database,
                func.sum(Profile.publication_count),
                func.sum(Profile.citation_count),
                func.sum(Profile.h_index),
                func.count(),
            ).
            group_by(Profile.scientometric_database)
        )).fetchall()
        
        return PublicationActivityResponse(
            items={
                item[0]: PublicationActivityItem(
                    total_publication_count = item[1],
                    total_citation_count    = item[2],
                    average_h_index         = item[3] / item[4],
                )
                for item in res 
            }
        )
