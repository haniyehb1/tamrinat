from fastapi import APIRouter, Body
from pydantic import BaseModel
import multiprocessing
import random
import time

router = APIRouter()

class ProcessInput(BaseModel):
    num_process: int

class MyProcess(multiprocessing.Process): # تعریف فرایند به عنوان زیرکلاس با اجرای ترتیبی
    def __init__(self, messages, name):
        super().__init__(name=name)
        self.messages = messages

    def run(self):
        self.messages.append('called run method by %s' % self.name)
        return

@router.post("/process5_1")
async def scenario1(process_input: ProcessInput = Body(...)):
    manager = multiprocessing.Manager()
    messages = manager.list()
    for i in range(1, process_input.num_process + 1):
        process = MyProcess(messages, f'MyProcess-{i}')
        process.start()
        process.join()
    return {"messages": list(messages)}

class MyProcesss(multiprocessing.Process): # اجرای تصادفی
    def __init__(self, messages, name):
        super().__init__(name=name)
        self.messages = messages

    def run(self):
        delay = random.randint(1, 5)
        time.sleep(delay)
        self.messages.append(f'called run method by {self.name}, delay={delay}')
        return

@router.post("/process5_2")
async def scenario2(process_input: ProcessInput = Body(...)):
    manager = multiprocessing.Manager()
    messages = manager.list()
    processs = []
    for i in range(1, process_input.num_process + 1):
        process = MyProcesss(messages, f'MyProcess-{i}')
        processs.append(process)
        process.start()
    for process in processs:
        process.join()
    return {"messages": list(messages)}

class MyProcessss(multiprocessing.Process): # اجرای ترتیبی با تاخیر
    def __init__(self, messages, name):
        super().__init__(name=name)
        self.messages = messages

    def run(self):
        delay = random.randint(1, 5)
        time.sleep(delay)
        self.messages.append(f'called run method by {self.name}, delay={delay}')
        return

@router.post("/process5_3")
async def scenario3(process_input: ProcessInput = Body(...)):
    manager = multiprocessing.Manager()
    messages = manager.list()
    for i in range(1, process_input.num_process + 1):
        process = MyProcessss(messages, f'MyProcess-{i}')
        process.start()
        process.join()
    return {"messages": list(messages)}



