from fastapi import APIRouter, Depends, HTTPException # importar do fast api o roteador
from src.models.goal_model import Goal
from src.api.dependencies import pegar_sessao
from src.schemas.goals_schemas import GoalsSchema


goals_router = APIRouter(prefix= "/goals", tags= ["metas"])

@goals_router.post("/criar metas")
async def create_goals(goals_schema: GoalsSchema, session = Depends(pegar_sessao)):
    new_goal = Goal(goals_schema.starting_date, goals_schema.ending_date, goals_schema.si_measurement_unit, goals_schema.value)
    session.add(new_goal)
    session.commit()
    return{"mensagem": "Meta cadastrada com sucesso"}


@goals_router.get("/listar ")
async def list_goals(session = Depends(pegar_sessao)):
    goals_list = session.query(GoalsSchema).all()
    if not goals_list:
        raise HTTPException(status_code=404, detail="Metas não encontradas")
    else:
        return{"mensagem": goals_list }

@goals_router.put("/editar meta_de_consumo")

@goals_router.delete("/deletar_meta/{id}")
async def delete_goals(id: int, session = Depends(pegar_sessao)):
    goals = session.query(GoalsSchema).filter(Goal. id == id).first()
    if not goals:
        raise HTTPException(status_code=404, detail="Metas não encontradas")
    else:
        session.delete(goals)
        session.commit()
        return {"mensagem": "Meta excluída com sucesso  "}
    

