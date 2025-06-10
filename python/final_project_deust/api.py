from fastapi import APIRouter
import crud
from fastapi import Request
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates
from pydantic import BaseModel


router = APIRouter()

class RobotCreate(BaseModel):
    name: str
    mission: str = "None" # "None" como valor predeterminado

# Configuración para templates
templates = Jinja2Templates(directory="templates")

@router.post("/robot/")
def create_robot(robot: RobotCreate):
    robot_id = crud.create_robot(robot.name, robot.mission)
    return {"uuid": robot_id}

@router.get("/", response_class=HTMLResponse)
async def read_root(request: Request):
    return templates.TemplateResponse("index.html", {"request": request})

@router.get("/robots/")
def list_robots():
    return crud.get_robots()

@router.get("/all_status/")
def get_all_status():
    return crud.get_status()

@router.post("/status/")
def update_status(robot_id: str, position: str, status: str):
    crud.add_status(robot_id, position, status)
    return {"message": "status ajouté"}

@router.get("/robot/{robot_id}/status")
def get_status(robot_id: str):
    return crud.get_last_status(robot_id)
