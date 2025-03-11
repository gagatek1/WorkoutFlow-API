from fastapi import FastAPI
from mangum import Mangum

from app.core.database import Base, engine

app = FastAPI(title="WorkoutFlow API", version="0.1.0")

handler = Mangum(app)

Base.metadata.create_all(engine)
