from fastapi import FastAPI, APIRouter, Path, Query
from pydantic import BaseModel
from multiprocessing import Process, Manager
import multiprocessing
import time
import random
from typing import List

app = FastAPI()
router = APIRouter()

class ScenarioInput(BaseModel):
    num_process: int = 6

def myFunc(i, messages):
    messages.append(f'calling myFunc from process n°: {i}')
    for j in range(0, i):
        messages.append(f'output from myFunc is :{j}')

def myFuncc(i, messages):
    messages.append(f'calling myFunc from process n°: {i}')
    time.sleep(random.uniform(0, 3))  # تاخیر تصادفی بین 0 تا 3 ثانیه
    for j in range(0, i):
        messages.append(f'output from myFunc is :{j}')

def scenario1(num_process: int):
    manager = multiprocessing.Manager()
    messages = manager.list()
    for i in range(num_process):
        process = multiprocessing.Process(target=myFunc, args=(i, messages))
        process.start()
        process.join()
    return list(messages)

def scenario2(num_process: int):
    manager = multiprocessing.Manager()
    messages = manager.list()
    processes = []
    for i in range(num_process):
        process = multiprocessing.Process(target=myFunc, args=(i, messages))
        processes.append(process)
        process.start()
    for process in processes:
        process.join()
    return list(messages)

def scenario3(num_process: int):
    manager = multiprocessing.Manager()
    messages = manager.list()
    processes = []
    for i in range(num_process):
        process = multiprocessing.Process(target=myFuncc, args=(i, messages))
        process.start()
        processes.append(process)
    for process in processes:
        process.join()
    return list(messages)

@router.post("/scenario11/{num_process}", response_model=List[str])
def run_scenario1_path(num_process: int = Path(..., title="Number of Processes")):
    return scenario1(num_process)

@router.post("/scenario11", response_model=List[str])
def run_scenario1_body(input: ScenarioInput):
    return scenario1(input.num_process)

@router.post("/scenario21/{num_process}", response_model=List[str])
def run_scenario2_path(num_process: int = Path(..., title="Number of Processes")):
    return scenario2(num_process)

@router.post("/scenario21", response_model=List[str])
def run_scenario2_body(input: ScenarioInput):
    return scenario2(input.num_process)

@router.post("/scenario31/{num_process}", response_model=List[str])
def run_scenario3_path(num_process: int = Path(..., title="Number of Processes")):
    return scenario3(num_process)

@router.post("/scenario31", response_model=List[str])
def run_scenario3_body(input: ScenarioInput):
    return scenario3(input.num_process)

app.include_router(router, prefix="/api", tags=["scenarios"])

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)

