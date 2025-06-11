from fastapi import FastAPI
from routers import farmgatepricerouter

app = FastAPI()
app.include_router(farmgatepricerouter)
