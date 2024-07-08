import time
import os
from random import randint
from threading import Thread
from fastapi import APIRouter
from pydantic import BaseModel
from typing import List

router = APIRouter()

class ThreadOutput(BaseModel):
    name: str
    message: str
    timestamp: float

results = []

class MyThreadClass(Thread):
    def __init__(self, name, duration):
        Thread.__init__(self)
        self.name = name
        self.duration = duration

    def run(self):
        global results
        start_message = f"---> {self.name} running, belonging to process ID {os.getpid()}"
        print(start_message)
        results.append(ThreadOutput(name=self.name, message=start_message, timestamp=time.time()))
        time.sleep(self.duration)
        end_message = f"---> {self.name} over"
        print(end_message)
        results.append(ThreadOutput(name=self.name, message=end_message, timestamp=time.time()))

def create_threads():
    threads = []
    for i in range(1, 10):
        thread = MyThreadClass(f"Thread#{i}", randint(1, 10))
        threads.append(thread)
    return threads

@router.post("/scenario1.3", response_model=List[ThreadOutput])
def run_scenario1():
    global results
    results = []

    threads = create_threads()
    for thread in threads:
        thread.start()
    for thread in threads:
        thread.join()

    return results

@router.post("/scenario2.3", response_model=List[ThreadOutput])
def run_scenario2():
    global results
    results = []

    threads = create_threads()
    even_threads = [t for i, t in enumerate(threads) if (i + 1) % 2 == 0]
    odd_threads = [t for i, t in enumerate(threads) if (i + 1) % 2 != 0]

    for thread in even_threads:
        thread.start()
    for thread in even_threads:
        thread.join()

    for thread in odd_threads:
        thread.start()
    for thread in odd_threads:
        thread.join()

    return results

@router.post("/scenario3.3", response_model=List[ThreadOutput])
def run_scenario3():
    global results
    results = []

    threads = create_threads()
    threads.reverse()

    for thread in threads:
        thread.start()
    for thread in threads:
        thread.join()

    return results
