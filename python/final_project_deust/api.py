from fastapi import APIRouter
import crud
from fastapi import Request
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates
from pydantic import BaseModel


router = APIRouter()

class RobotCreate(BaseModel):
    name: str
    addressMac: str
    mission: str = "None" # "None" como valor predeterminado

class DeleteRobot(BaseModel):
    robot_id: str

class RobotInstruction(BaseModel):
    robot_id: str
    instruction: str

class RobotInstructionForDelete(BaseModel):
    robot_id: str

class RobotStatus(BaseModel):
    robot_id: str
    position: str
    status: str

class RobotDataByMacAddress(BaseModel):
    mac_address: str

# Configuración para templates
templates = Jinja2Templates(directory="templates")

@router.get("/", response_class=HTMLResponse)               # ROOT ENDPOINT
async def read_root(request: Request):
    return templates.TemplateResponse("index.html", {"request": request})


@router.post("/robot/")                                     # CREATE A ROBOT
def create_robot(robot: RobotCreate):
    robot_id = crud.create_robot(robot.name, robot.addressMac,robot.mission)
    return {"uuid": robot_id}

@router.post("/delete_robot/")                              # DELETE A ROBOT BY ID
def delete_robot(robot: DeleteRobot):
    crud.delete_robot(robot.robot_id)
    return {"message": "robot supprimé"}

@router.get("/robots/")                                     # LIST ALL ROBOTS  
def list_robots():
    return crud.get_robots()

@router.get("/all_status/")                                  # LIST ALL STATUS
def get_all_status():
    return crud.get_status()

@router.post("/update_status/")                              # UPDATE STATUS OF A ROBOT   
def update_status(status: RobotStatus):
    crud.add_status(status.robot_id, status.position, status.status)
    return {"message": "status ajouté"}

@router.get("/robot/{robot_id}/status")                      # GET LAST STATUS OF A ROBOT    
def get_status(robot_id: str):
    return crud.get_last_status(robot_id)

@router.post("/robot_data_by_mac_address")                    # GET THE ROBOT DATA BY HIS MAC ADDRESS
def get_robot_data_by_mac_address(robotMacAddress: RobotDataByMacAddress):
    return crud.get_robot_data_by_mac_address(robotMacAddress.mac_address)

@router.get('/instructions')
def get_instructions(robot_id: str):
    return crud.get_instructions(robot_id)

@router.post('/create_instruction')
def create_instruction(robot_instruction: RobotInstruction):
    return crud.create_instruction(robot_instruction.robot_id, robot_instruction.instruction) 

@router.post('/delete_instruction')
def delete_instruction(robot_instruction: RobotInstructionForDelete):
    return crud.delete_instruction(robot_instruction.robot_id)