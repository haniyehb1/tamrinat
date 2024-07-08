from fastapi import FastAPI, APIRouter, Body
from pydantic import BaseModel
import multiprocessing
import random
import time

app = FastAPI()
router = APIRouter()

class Producer(multiprocessing.Process):
    def __init__(self, queue, messages):
        multiprocessing.Process.__init__(self)
        self.queue = queue
        self.messages = messages

    def run(self):
        for i in range(10):
            item = random.randint(0, 256)
            self.queue.put(item)
            self.messages.append(f"Process Producer: item {item} appended to queue {self.name}")
            time.sleep(1)
            self.messages.append(f"The size of queue is {self.queue.qsize()}")
            if (i + 1) % 3 == 0:
                time.sleep(2)

class Consumer(multiprocessing.Process):
    def __init__(self, queue, messages):
        multiprocessing.Process.__init__(self)
        self.queue = queue
        self.messages = messages

    def run(self):
        while True:
            if self.queue.empty():
                self.messages.append("The queue is empty")
                break
            else:
                time.sleep(2)
                item = self.queue.get()
                self.messages.append(f"Process Consumer: item {item} popped from {self.name}")
                time.sleep(1)

class Producer2(multiprocessing.Process):
    def __init__(self, queue, messages):
        multiprocessing.Process.__init__(self)
        self.queue = queue
        self.messages = messages

    def run(self):
        for i in range(10):
            item = random.randint(0, 256)
            self.queue.put(item)
            self.messages.append(f"Process Producer: item {item} appended to queue {self.name}")
            time.sleep(1)
            self.messages.append(f"The size of queue is {self.queue.qsize()}")
            if i % 2 == 0:
                time.sleep(2)

class Consumer2(multiprocessing.Process):
    def __init__(self, queue, messages):
        multiprocessing.Process.__init__(self)
        self.queue = queue
        self.messages = messages

    def run(self):
        while True:
            if self.queue.empty():
                self.messages.append("The queue is empty")
                break
            else:
                item = self.queue.get()
                self.messages.append(f"Process Consumer: item {item} popped from {self.name}")
                time.sleep(1)

class Producer3(multiprocessing.Process):
    def __init__(self, queue, messages):
        multiprocessing.Process.__init__(self)
        self.queue = queue
        self.messages = messages

    def run(self):
        for i in range(10):
            item = random.randint(0, 256)
            self.queue.put(item)
            self.messages.append(f"Process Producer: item {item} appended to queue {self.name}")
            time.sleep(1)
            self.messages.append(f"The size of queue is {self.queue.qsize()}")

class Consumer3(multiprocessing.Process):
    def __init__(self, queue, messages):
        multiprocessing.Process.__init__(self)
        self.queue = queue
        self.messages = messages

    def run(self):
        while True:
            if self.queue.empty():
                self.messages.append("The queue is empty")
                break
            else:
                time.sleep(2)
                item = self.queue.get()
                self.messages.append(f"Process Consumer: item {item} popped from {self.name}")
                time.sleep(1)

class ProcessInput(BaseModel):
    scenario: int

@router.post("/process6_1/", response_model=dict)
async def scenario_1(input: ProcessInput = Body(...)):
    manager = multiprocessing.Manager()
    messages = manager.list()
    queue = multiprocessing.Queue()
    process_producer = Producer(queue, messages)
    process_consumer = Consumer(queue, messages)
    process_producer.start()
    process_consumer.start()
    process_producer.join()
    process_consumer.join()
    return {"messages": list(messages)}

@router.post("/process6_2/", response_model=dict)
async def scenario_2(input: ProcessInput = Body(...)):
    manager = multiprocessing.Manager()
    messages = manager.list()
    queue = multiprocessing.Queue()
    process_producer = Producer2(queue, messages)
    process_consumer = Consumer2(queue, messages)
    process_producer.start()
    process_consumer.start()
    process_producer.join()
    process_consumer.join()
    return {"messages": list(messages)}

@router.post("/process6_3/", response_model=dict)
async def scenario_3(input: ProcessInput = Body(...)):
    manager = multiprocessing.Manager()
    messages = manager.list()
    queue = multiprocessing.Queue()
    process_producer = Producer3(queue, messages)
    process_consumer = Consumer3(queue, messages)
    process_producer.start()
    process_producer.join()
    process_consumer.start()
    process_consumer.join()
    return {"messages": list(messages)}

app.include_router(router, tags=["scenarios"])

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)




