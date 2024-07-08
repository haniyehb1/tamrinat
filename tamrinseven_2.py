from fastapi import FastAPI, APIRouter, Query, Body
from pydantic import BaseModel
import multiprocessing
from multiprocessing import Barrier, Lock, Process
from time import time
from datetime import datetime

app = FastAPI()
router = APIRouter()

class ScenarioInput(BaseModel):
    synchronizer_count: int = 2

def test_with_barrier(synchronizer, serializer, output):
    name = multiprocessing.current_process().name
    synchronizer.wait()
    now = time()
    with serializer:
        timestamp = datetime.fromtimestamp(now)
        print(f"process {name} ----> {timestamp}")
        output.append(f"process {name} ----> {timestamp}")

def test_without_barrier(output):
    name = multiprocessing.current_process().name
    now = time()
    timestamp = datetime.fromtimestamp(now)
    print(f"process {name} ----> {timestamp}")
    output.append(f"process {name} ----> {timestamp}")

@router.post("/scenario-17", response_model=dict)
async def scenario_16(input: ScenarioInput = Body(...)):
    synchronizer = Barrier(input.synchronizer_count)
    serializer = Lock()
    manager = multiprocessing.Manager()
    output = manager.list()

    processes = [
        Process(name='p1 - test_with_barrier', target=test_with_barrier, args=(synchronizer, serializer, output)),
        Process(name='p2 - test_with_barrier', target=test_with_barrier, args=(synchronizer, serializer, output)),
        Process(name='p3 - test_without_barrier', target=test_without_barrier, args=(output,)),
        Process(name='p4 - test_without_barrier', target=test_without_barrier, args=(output,))
    ]

    for process in processes:
        process.start()
    for process in processes:
        process.join()

    return {"scenario": 17, "output": list(output)}

@router.post("/scenario-27", response_model=dict)
async def scenario_26(input: ScenarioInput = Body(...)):
    synchronizer = Barrier(input.synchronizer_count)
    serializer = Lock()
    manager = multiprocessing.Manager()
    output = manager.list()

    processes = [
        Process(name='p1 - test_with_barrier', target=test_with_barrier, args=(synchronizer, serializer, output)),
        Process(name='p2 - test_with_barrier', target=test_with_barrier, args=(synchronizer, serializer, output)),
        Process(name='p3 - test_with_barrier', target=test_with_barrier, args=(synchronizer, serializer, output)),
        Process(name='p4 - test_without_barrier', target=test_without_barrier, args=(output,))
    ]

    for process in processes:
        process.start()
    for process in processes:
        process.join()

    return {"scenario": 27, "output": list(output)}

@router.post("/scenario-37", response_model=dict)
async def scenario_36(input: ScenarioInput = Body(...)):
    synchronizer = Barrier(input.synchronizer_count)
    serializer = Lock()
    manager = multiprocessing.Manager()
    output = manager.list()

    processes = [
        Process(name='p1 - test_with_barrier', target=test_with_barrier, args=(synchronizer, serializer, output)),
        Process(name='p2 - test_with_barrier', target=test_with_barrier, args=(synchronizer, serializer, output)),
        Process(name='p3 - test_with_barrier', target=test_with_barrier, args=(synchronizer, serializer, output)),
        Process(name='p4 - test_with_barrier', target=test_with_barrier, args=(synchronizer, serializer, output))
    ]

    for process in processes:
        process.start()
    for process in processes:
        process.join()

    return {"scenario": 37, "output": list(output)}

app.include_router(router)

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)

