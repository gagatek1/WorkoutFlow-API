from fastapi import FastAPI
from mangum import Mangum

app = FastAPI(title="WorkoutFlow API", version="0.1.0")

handler = Mangum(app)
