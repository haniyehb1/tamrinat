from fastapi import APIRouter
from pydantic import BaseModel
from random import randrange
from threading import Barrier, Thread, Lock
from time import ctime, sleep
from typing import List

router = APIRouter()

class ScenarioInput(BaseModel):
    num_runners: int = 3
    runners: List[str] = ["Huey", "Dewey", "Louie"]

class ScenarioOutput(BaseModel):
    message: str
    details: List[str]

@router.post("/scenario1.7", response_model=ScenarioOutput)
def scenario1(input: ScenarioInput):
    num_runners = input.num_runners
    runners = input.runners.copy()
    finish_line = Barrier(num_runners)
    results = []

    def runner():
        nonlocal runners
        name = runners.pop()
        sleep(randrange(2, 5))
        results.append(f'{name} reached the barrier at: {ctime()}')
        finish_line.wait()

    threads = []
    results.append('START RACE!!!!')
    for i in range(num_runners):
        thread = Thread(target=runner)
        threads.append(thread)
        thread.start()
    for thread in threads:
        thread.join()
    results.append('Race over!')

    return {"message": "Scenario 1 completed successfully", "details": results}

@router.post("/scenario2.7", response_model=ScenarioOutput)
def scenario2(input: ScenarioInput):
    num_runners = input.num_runners
    runners = input.runners.copy()
    finish_line = Barrier(num_runners)
    results = []
    lock = Lock()

    def runner():
        nonlocal runners
        with lock:
            name = runners.pop()
        sleep(randrange(1, 5))
        results.append(f'{name} reached the barrier at: {ctime()}')
        finish_line.wait()

    threads = []
    results.append('START RACE!!!!')
    for i in range(num_runners):
        thread = Thread(target=runner)
        threads.append(thread)
        thread.start()
    for thread in threads:
        thread.join()
    results.append('Race over!')

    return {"message": "Scenario 2 completed successfully", "details": results}

@router.post("/scenario3.7", response_model=ScenarioOutput)
def scenario3(input: ScenarioInput):
    num_runners = input.num_runners
    runners = input.runners.copy()
    finish_line = Barrier(num_runners)
    results = []

    def runner():
        nonlocal runners
        name = runners.pop()
        sleep(randrange(2, 5))
        finish_line.wait()
        results.append(f'{name} reached the barrier at: {ctime()}')

    threads = []
    results.append('START RACE!!!!')
    for i in range(num_runners):
        thread = Thread(target=runner)
        threads.append(thread)
        thread.start()
    for thread in threads:
        thread.join()
    results.append('Race over!')

    return {"message": "Scenario 3 completed successfully", "details": results}