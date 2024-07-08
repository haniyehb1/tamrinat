from fastapi import APIRouter, Query
from pydantic import BaseModel
import threading
import time
import os
from random import randint
from typing import List

router = APIRouter()

# Lock Definition
threadLock = threading.Lock()

class ThreadOutput(BaseModel):
    name: str
    message: str
    timestamp: float

results = []

class MyThreadClass(threading.Thread):
    def __init__(self, name, duration):
        threading.Thread.__init__(self)
        self.name = name
        self.duration = duration

    def run(self):
        global results
        # Acquire the Lock
        threadLock.acquire()
        start_message = f"---> {self.name} running, belonging to process ID {os.getpid()}"
        print(start_message)
        results.append(ThreadOutput(name=self.name, message=start_message, timestamp=time.time()))
        time.sleep(self.duration)
        end_message = f"---> {self.name} over"
        print(end_message)
        results.append(ThreadOutput(name=self.name, message=end_message, timestamp=time.time()))
        # Release the Lock
        threadLock.release()

def create_threads(count: int):
    threads = []
    for i in range(1, count + 1):
        thread = MyThreadClass(f"Thread#{i}", randint(1, 10))
        threads.append(thread)
    return threads

# Scenario 1: Execute and join threads one by one
@router.post("/scenario1.4", response_model=List[ThreadOutput])
def run_scenario1(count: int = Query(9)):
    global results
    results = []

    threads = create_threads(count)
    for thread in threads:
        thread.start()
        thread.join()

    return results

# Scenario 2: Execute even threads first, then odd threads
@router.post("/scenario2.4", response_model=List[ThreadOutput])
def run_scenario2(count: int = Query(9)):
    global results
    results = []

    threads = create_threads(count)
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

# Scenario 3: Execute threads in reverse order
@router.post("/scenario3.4", response_model=List[ThreadOutput])
def run_scenario3(count: int = Query(9)):
    global results
    results = []

    threads = create_threads(count)
    threads.reverse()

    for thread in threads:
        thread.start()
    for thread in threads:
        thread.join()

    return results

