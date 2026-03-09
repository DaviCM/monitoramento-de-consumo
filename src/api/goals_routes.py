from fastapi import APIRouter, Depends, HTTPException # importar do fast api o roteador
from src.models.goal_model import Goal
from src.api.dependencies import pegar_sessao
from src.schemas.goals_schemas import GoalsSchema, UpdateGoalsSchema


goals_router = APIRouter(prefix= "/goals", tags= ["metas"])

@goals_router.post("/criar_metas")
async def create_goals(goals_schema: GoalsSchema, session = Depends(pegar_sessao)):
     new_goal = Goal(
    starting_date=goals_schema.starting_date,
    ending_date=goals_schema.ending_date,
    si_measurement_unit=goals_schema.si_measurement_unit,
    value=goals_schema.value
)
     session.add(new_goal)
     session.commit()
     return{"mensagem": "Meta cadastrada com sucesso"}


@goals_router.get("/listar_metas")
async def list_goals(session = Depends(pegar_sessao)):
    goals_list = session.query(GoalsSchema).all()
    if not goals_list:
        raise HTTPException(status_code=404, detail="Metas não encontradas")
    else:
        return{"mensagem": goals_list }

@goals_router.put("/editar_meta_de_consumo")
async def change_consumption(goals_schema: UpdateGoalsSchema , session = Depends(pegar_sessao)):
    goal = session.query(Goal).filter(Goal.id == goals_schema.id).first()
    if not goal:
        raise HTTPException(status_code=404, detail = "Registros de consumo não encontrado")
    if goals_schema.new_starting_date is not None:
            goal.starting_date = goals_schema.new_starting_date
    if goals_schema.new_ending_date is not None:
            goal.ending_date = goals_schema.new_ending_date
    if goals_schema.new_si_measurement_unit is not None:
            goal.si_measurement_unit = goals_schema.new_si_measurement_unit
    if goals_schema.value is not None:
            goal.value = goals_schema.new_value
    session.commit()
    return{"mensagem" : "Metas de consumo alterados com sucesso"}

@goals_router.delete("/deletar_meta/{id}")
async def delete_goals(id: int, session = Depends(pegar_sessao)):
    goals = session.query(Goal).filter(Goal. id == id).first()
    if not goals:
        raise HTTPException(status_code=404, detail="Metas não encontradas")
    else:
        session.delete(goals)
        session.commit()
        return {"mensagem": "Meta excluída com sucesso  "}
    

