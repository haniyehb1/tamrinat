from fastapi import APIRouter
from typing import List
from pydantic import BaseModel
import threading
import time

router = APIRouter()

class ThreadOutput(BaseModel):
    thread_number: str
    message: str
    timestamp: float

results = []

def function_A(local_results):
    message = f'{threading.currentThread().getName()} --> starting'
    timestamp = time.time()
    local_results.append(ThreadOutput(thread_number='function_A', message=message, timestamp=timestamp))
    time.sleep(2)
    message = f'{threading.currentThread().getName()} --> exiting'
    timestamp = time.time()
    local_results.append(ThreadOutput(thread_number='function_A', message=message, timestamp=timestamp))

def function_B(local_results):
    message = f'{threading.currentThread().getName()} --> starting'
    timestamp = time.time()
    local_results.append(ThreadOutput(thread_number='function_B', message=message, timestamp=timestamp))
    time.sleep(2)
    message = f'{threading.currentThread().getName()} --> exiting'
    timestamp = time.time()
    local_results.append(ThreadOutput(thread_number='function_B', message=message, timestamp=timestamp))

def function_C(local_results):
    message = f'{threading.currentThread().getName()} --> starting'
    timestamp = time.time()
    local_results.append(ThreadOutput(thread_number='function_C', message=message, timestamp=timestamp))
    time.sleep(2)
    message = f'{threading.currentThread().getName()} --> exiting'
    timestamp = time.time()
    local_results.append(ThreadOutput(thread_number='function_C', message=message, timestamp=timestamp))

@router.post("/scenario1.2", response_model=List[ThreadOutput])
def run_scenario1():
    global results
    results = []

    local_results = []

    t1 = threading.Thread(target=function_A, args=(local_results,))
    t2 = threading.Thread(target=function_B, args=(local_results,))
    t3 = threading.Thread(target=function_C, args=(local_results,))

    t1.start()
    t1.join()
    t2.start()
    t2.join()
    t3.start()
    t3.join()

    results.extend(local_results)
    return results

@router.post("/scenario2.2", response_model=List[ThreadOutput])
def run_scenario2():
    global results
    results = []

    local_results = []

    t1 = threading.Thread(target=function_A, args=(local_results,))
    t2 = threading.Thread(target=function_B, args=(local_results,))
    t3 = threading.Thread(target=function_C, args=(local_results,))

    t1.start()
    t2.start()
    t1.join()
    t2.join()

    t3.start()
    t3.join()

    results.extend(local_results)
    return results

@router.post("/scenario3.2", response_model=List[ThreadOutput])
def run_scenario3():
    global results
    results = []

    local_results = []

    t1 = threading.Thread(target=function_C, args=(local_results,))
    t2 = threading.Thread(target=function_B, args=(local_results,))
    t3 = threading.Thread(target=function_A, args=(local_results,))

    t1.start()
    t1.join()
    t2.start()
    t2.join()
    t3.start()
    t3.join()

    results.extend(local_results)
    return results
