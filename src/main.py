from fastapi import FastAPI

from .routers.profiles.router import router as profiles_router
from .routers.analytics.router import router as analytics_router


appV1 = FastAPI(title="FEFU Analytics Sector", description="Test task for python backend developer", version="1.0")
appV1.include_router(profiles_router, tags=["profiles"])
appV1.include_router(analytics_router, tags=["analytics"])

app = FastAPI()
app.mount("/v1", appV1)
