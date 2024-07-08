import threading
import time
import random
from fastapi import FastAPI, APIRouter, Body
from pydantic import BaseModel, Field
import logging

app = FastAPI()

LOG_FORMAT = '%(asctime)s %(threadName)-17s %(levelname)-8s %(message)s'
logging.basicConfig(level=logging.INFO, format=LOG_FORMAT)
semaphore = threading.Semaphore(0)

class ScenarioOutput(BaseModel):
    logs: list[str]

class Items(BaseModel):
    number_of_steps: int

router = APIRouter()

# Scenario 1: اجرای یک در میان تولید و مصرف کننده
@router.post("/scenario1.6", response_model=ScenarioOutput)
async def scenario1(items: Items = Body(...)):
    logs = []
    item = 0

    def consumer():
        nonlocal item
        logs.append(f"{time.strftime('%Y-%m-%d %H:%M:%S')} {threading.current_thread().name} INFO Consumer is waiting")
        semaphore.acquire()
        logs.append(f"{time.strftime('%Y-%m-%d %H:%M:%S')} {threading.current_thread().name} INFO Consumer notify: item number {item}")

    def producer():
        nonlocal item
        time.sleep(3)
        item = random.randint(0, 1000)
        logs.append(f"{time.strftime('%Y-%m-%d %H:%M:%S')} {threading.current_thread().name} INFO Producer notify: item number {item}")
        semaphore.release()

    for i in range(items.number_of_steps):
        t1 = threading.Thread(target=consumer)
        t2 = threading.Thread(target=producer)
        t1.start()
        t2.start()
        t1.join()
        t2.join()

    return {"logs": logs}

# Scenario 2: برداشتن جوین ها و انتظار همیشگی مصرف کننده به اندازه گام ها
@router.post("/scenario2.6", response_model=ScenarioOutput)
async def scenario2(items: Items = Body(...)):
    logs = []
    item = 0

    def consumer():
        nonlocal item
        logs.append(f"{time.strftime('%Y-%m-%d %H:%M:%S')} {threading.current_thread().name} INFO Consumer is waiting")
        semaphore.acquire()
        logs.append(f"{time.strftime('%Y-%m-%d %H:%M:%S')} {threading.current_thread().name} INFO Consumer notify: item number {item}")

    def producer():
        nonlocal item
        time.sleep(3)
        item = random.randint(0, 1000)
        logs.append(f"{time.strftime('%Y-%m-%d %H:%M:%S')} {threading.current_thread().name} INFO Producer notify: item number {item}")
        semaphore.release()

    for i in range(items.number_of_steps):
        t1 = threading.Thread(target=consumer)
        t2 = threading.Thread(target=producer)
        t1.start()
        t2.start()

    return {"logs": logs}

# Scenario 3: اجرای متوالی تولید کننده و از دست رفتن محتوای آیتم قبل از مصرف
@router.post("/scenario3.6", response_model=ScenarioOutput)
async def scenario3(items: Items = Body(...)):
    logs = []
    item = 0

    def consumer():
        nonlocal item
        logs.append(f"{time.strftime('%Y-%m-%d %H:%M:%S')} {threading.current_thread().name} INFO Consumer is waiting")
        semaphore.acquire()
        logs.append(f"{time.strftime('%Y-%m-%d %H:%M:%S')} {threading.current_thread().name} INFO Consumer notify: item number {item}")

    def producer():
        nonlocal item
        time.sleep(3)
        item = random.randint(0, 1000)
        logs.append(f"{time.strftime('%Y-%m-%d %H:%M:%S')} {threading.current_thread().name} INFO Producer notify: item number {item}")
        semaphore.release()

    # تولید کننده همه آیتم‌ها را تولید می‌کند به اندازه تعداد مراحل
    for i in range(items.number_of_steps):
        t2 = threading.Thread(target=producer)
        t2.start()
        t2.join()

    # مصرف کننده آیتم نهایی را مصرف می‌کند به اندازه تعداد مراحل
    for i in range(items.number_of_steps):
        t1 = threading.Thread(target=consumer)
        t1.start()
        t1.join()

    return {"logs": logs}

app.include_router(router)

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)

