from fastapi import FastAPI, APIRouter, Body
from pydantic import BaseModel
import multiprocessing
import time

app = FastAPI()
router = APIRouter()

class ProcessInput(BaseModel):
    name: str

def foo(messages):
    name = multiprocessing.current_process().name
    messages.append("Starting %s " % name)
    if name == 'background_process':
        for i in range(0, 5):
            messages.append('---> %d ' % i)
        time.sleep(1)
    else:
        for i in range(5, 10):
            messages.append('---> %d ' % i)
        time.sleep(1)
    messages.append("Exiting %s " % name)

@router.post("/process/scenario-13/", response_model=dict)
async def scenario1(process_input: ProcessInput = Body(...)):
    manager = multiprocessing.Manager()
    messages = manager.list()
    background_process = multiprocessing.Process(name='background_process', target=foo, args=(messages,))
    background_process.daemon = True
    NO_background_process = multiprocessing.Process(name='NO_background_process', target=foo, args=(messages,))
    NO_background_process.daemon = False
    background_process.start()
    NO_background_process.start()
    background_process.join()
    NO_background_process.join()
    return {"messages": list(messages)}

@router.post("/process/scenario-23/", response_model=dict)
async def scenario2(process_input: ProcessInput = Body(...)):
    manager = multiprocessing.Manager()
    messages = manager.list()
    background_process = multiprocessing.Process(name='background_process', target=foo, args=(messages,))
    background_process.daemon = True
    NO_background_process = multiprocessing.Process(name='NO_background_process', target=foo, args=(messages,))
    NO_background_process.daemon = False
    background_process.start()
    NO_background_process.start()
    background_process.join()
    NO_background_process.join()
    return {"messages": list(messages)}

@router.post("/process/scenario-33/", response_model=dict)
async def scenario3(process_input: ProcessInput = Body(...)):
    manager = multiprocessing.Manager()
    messages = manager.list()
    background_process = multiprocessing.Process(name='background_process', target=foo, args=(messages,))
    background_process.daemon = True
    NO_background_process = multiprocessing.Process(name='NO_background_process', target=foo, args=(messages,))
    NO_background_process.daemon = False
    background_process.start()
    NO_background_process.start()
    background_process.join()
    NO_background_process.join()
    return {"messages": list(messages)}

app.include_router(router)
