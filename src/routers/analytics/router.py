from fastapi import APIRouter

from .schemas import PublicationActivityResponse
from .service import publication_activity__calculate


router = APIRouter(prefix="/analytics")


@router.get(
    "/publication_activity/calculate", 
    response_model=PublicationActivityResponse,
    responses={
        200: {
            "content": {
                "application/json": {
                    "example": {
                        "items": {
                            "Scopus": {
                                "total_publication_count": 3368,
                                "total_citation_count": 177083,
                                "average_h_index": 62.6,
                            },
                        },
                    },
                },
            },
        },
    },
)
async def publication_activity():
    return await publication_activity__calculate()
