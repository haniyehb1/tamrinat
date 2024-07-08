from fastapi import FastAPI, APIRouter, Body
from pydantic import BaseModel
import multiprocessing
import time

app = FastAPI()
router = APIRouter()

class ProcessInput(BaseModel):
    name: str

def foo1(messages):
    messages.append('Starting function')
    for i in range(10):
        messages.append('-->%d\n' % i)
        time.sleep(1)
    messages.append('Finished function')

@router.post("/process/scenario-14/", response_model=dict)
async def scenario1(process_input: ProcessInput = Body(...)):
    manager = multiprocessing.Manager()
    messages = manager.list()
    p = multiprocessing.Process(target=foo1, args=(messages,))
    messages.append(f'Process before execution: {p} {p.is_alive()}')
    p.start()
    messages.append(f'Process running: {p} {p.is_alive()}')
    p.terminate()
    messages.append(f'Process terminated: {p} {p.is_alive()}')
    p.join()
    messages.append(f'Process joined: {p} {p.is_alive()}')
    messages.append(f'Process exit code: {p.exitcode}')
    return {"messages": list(messages)}

@router.post("/process/scenario-24/", response_model=dict)
async def scenario2(process_input: ProcessInput = Body(...)):
    manager = multiprocessing.Manager()
    messages = manager.list()
    p = multiprocessing.Process(target=foo1, args=(messages,))
    messages.append(f'Process before execution: {p} {p.is_alive()}')
    p.start()
    messages.append(f'Process running: {p} {p.is_alive()}')
    p.terminate()
    time.sleep(0.1)
    messages.append(f'Process terminated: {p} {p.is_alive()}')
    p.join()
    messages.append(f'Process joined: {p} {p.is_alive()}')
    messages.append(f'Process exit code: {p.exitcode}')
    return {"messages": list(messages)}

@router.post("/process/scenario-34/", response_model=dict)
async def scenario3(process_input: ProcessInput = Body(...)):
    manager = multiprocessing.Manager()
    messages = manager.list()
    p = multiprocessing.Process(target=foo1, args=(messages,))
    messages.append(f'Process before execution: {p} {p.is_alive()}')
    p.start()
    messages.append(f'Process running: {p} {p.is_alive()}')
    time.sleep(5)
    p.terminate()
    time.sleep(0.1)
    messages.append(f'Process terminated: {p} {p.is_alive()}')
    p.join()
    messages.append(f'Process joined: {p} {p.is_alive()}')
    messages.append(f'Process exit code: {p.exitcode}')
    return {"messages": list(messages)}

app.include_router(router)

