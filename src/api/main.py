from fastapi import FastAPI
from consumption_real_routes import consumption_real_router
from goals_routes import goals_router
from user_routes import user_router
from consumption_simulation_routes import consumption_simulation_router


app =  FastAPI()

app.include_router(consumption_real_router)
app.include_router(consumption_simulation_router)
app.include_router(user_router)
app.include_router(goals_router)
