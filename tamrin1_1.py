from fastapi import APIRouter
from pydantic import BaseModel
import threading
import time

router = APIRouter()

class ThreadOutput(BaseModel):
    thread_number: int
    message: str
    timestamp: float

# Define a list to store results temporarily
results = []

def my_func(thread_number):
    message = f'my_func called by thread N°{thread_number}'
    timestamp = time.time()  # Record the timestamp
    time.sleep(1)  # Simulate some computation time
    results.append(ThreadOutput(thread_number=thread_number, message=message, timestamp=timestamp))

@router.post("/scenario1", response_model=list[ThreadOutput])
async def run_scenario1():
    global results
    results = []  # Clear previous results
    threads = []
    for i in range(10):
        t = threading.Thread(target=my_func, args=(i,))
        threads.append(t)
        t.start()

    # Wait for all threads to finish
    for t in threads:
        t.join()

    # Sort results by thread_number
    sorted_results = sorted(results, key=lambda x: x.thread_number)
    return sorted_results

@router.post("/scenario2", response_model=list[ThreadOutput])
async def run_scenario2():
    global results
    results = []  # Clear previous results
    threads = []

    # Create and start threads for even numbers first
    even_threads = []
    for i in range(0, 10, 2):
        t = threading.Thread(target=my_func, args=(i,))
        even_threads.append(t)
        threads.append(t)
        t.start()

    # Wait for all even threads to finish
    for t in even_threads:
        t.join()

    # Create and start threads for odd numbers
    odd_threads = []
    for i in range(1, 10, 2):
        t = threading.Thread(target=my_func, args=(i,))
        odd_threads.append(t)
        threads.append(t)
        t.start()

    # Wait for all odd threads to finish
    for t in odd_threads:
        t.join()

    return results

@router.post("/scenario3", response_model=list[ThreadOutput])
async def run_scenario3():
    global results
    results = []  # Clear previous results
    threads = []
    for i in range(9, -1, -1):
        t = threading.Thread(target=my_func, args=(i,))
        threads.append(t)
        t.start()

    # Wait for all threads to finish
    for t in threads:
        t.join()

    # Sort results by thread_number in descending order
    sorted_results = sorted(results, key=lambda x: x.thread_number, reverse=True)
    return sorted_results
