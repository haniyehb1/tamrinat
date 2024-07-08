from fastapi import FastAPI, APIRouter, Body
from pydantic import BaseModel
import multiprocessing
import time

app = FastAPI()
router = APIRouter()

class ProcessInput(BaseModel):
    name: str

def myFunc1(messages):
    name = multiprocessing.current_process().name
    messages.append("Starting process name = %s" % name)
    time.sleep(3)
    messages.append("Exiting process name = %s" % name)

@router.post("/scenario_12/")  # تغییر: استفاده از POST به جای GET
async def scenario1(process_input: ProcessInput = Body(...)):
    manager = multiprocessing.Manager()
    messages = manager.list()
    process1 = multiprocessing.Process(name='myFunc process', target=myFunc1, args=(messages,))
    process2 = multiprocessing.Process(target=myFunc1, args=(messages,))
    process1.start()
    process2.start()
    process1.join()
    process2.join()
    return {"messages": list(messages)}

@router.post("/scenario_22/")  # تغییر: استفاده از POST به جای GET
async def scenario2(process_input: ProcessInput = Body(...)):
    manager = multiprocessing.Manager()
    messages = manager.list()
    process1 = multiprocessing.Process(name='myFunc process', target=myFunc1, args=(messages,))
    process2 = multiprocessing.Process(target=myFunc1, args=(messages,))
    process1.start()
    process1.join()
    process2.start()
    process2.join()
    return {"messages": list(messages)}

def myFunc2(messages, delay):
    name = multiprocessing.current_process().name
    messages.append("Starting process name = %s" % name)
    time.sleep(delay)
    messages.append("Exiting process name = %s" % name)

@router.post("/scenario_32/")  # تغییر: استفاده از POST به جای GET
async def scenario3(process_input: ProcessInput = Body(...)):
    manager = multiprocessing.Manager()
    messages = manager.list()
    process1 = multiprocessing.Process(name='myFunc process', target=myFunc2, args=(messages, 2))
    process2 = multiprocessing.Process(target=myFunc2, args=(messages, 1))
    process1.start()
    process2.start()
    process1.join()
    process2.join()
    return {"messages": list(messages)}

app.include_router(router)




