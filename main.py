from fastapi import FastAPI
from mangum import Mangum

from app.api.v1.router import router
from app.core.database import Base, engine

app = FastAPI(title="WorkoutFlow API", version="0.3.0")

handler = Mangum(app)

Base.metadata.create_all(engine)
app.include_router(router)
