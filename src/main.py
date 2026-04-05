from fastapi import FastAPI
from src.api.consumption_real_routes import consumption_real_router
from src.api.goals_routes import goals_router
from src.api.user_routes import user_router
# from src.api.consumption_simulation_routes import consumption_simulation_router


app =  FastAPI()

app.include_router(consumption_real_router)

app.include_router(user_router)
app.include_router(goals_router)
