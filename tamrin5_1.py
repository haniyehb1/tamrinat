import threading
import time
from fastapi import FastAPI, APIRouter
from pydantic import BaseModel
from typing import List, Dict

app = FastAPI()
router = APIRouter()

class Box:
    def __init__(self):
        self.lock = threading.RLock()
        self.total_items = 0

    def execute(self, value):
        with self.lock:
            self.total_items += value

    def add(self):
        with self.lock:
            self.execute(1)

    def remove(self):
        with self.lock:
            self.execute(-1)

def adder(box: Box, items: int, results: List[Dict]):
    results.append({"message": f"N° {items} items to ADD"})
    while items > 0:
        box.add()
        time.sleep(1)
        items -= 1
        results.append({"message": f"ADDED one item --> {items} item to ADD"})

def remover(box: Box, items: int, results: List[Dict]):
    results.append({"message": f"N° {items} items to REMOVE"})
    while items > 0:
        box.remove()
        time.sleep(1)
        items -= 1
        results.append({"message": f"REMOVED one item --> {items} item to REMOVE"})

class ScenarioInput(BaseModel):
    add_items: int
    remove_items: int

@router.post("/scenario1.5/", response_model=List[Dict])
def run_scenario1_5(body: ScenarioInput):
    box = Box()
    results = []

    t1 = threading.Thread(target=adder, args=(box, body.add_items, results))
    t2 = threading.Thread(target=remover, args=(box, body.remove_items, results))

    t1.start()
    t2.start()

    t1.join()
    t2.join()

    return results

@router.post("/scenario2.5/", response_model=List[Dict])
def run_scenario2_5(body: ScenarioInput):
    box = Box()
    results = []

    t1 = threading.Thread(target=adder, args=(box, body.add_items, results))
    t2 = threading.Thread(target=remover, args=(box, body.remove_items, results))

    t1.start()
    t1.join()

    t2.start()
    t2.join()

    return results[::-1]

@router.post("/scenario3.5/", response_model=List[Dict])
def run_scenario3_5(body: ScenarioInput):
    box = Box()
    results = []

    t1 = threading.Thread(target=remover, args=(box, body.remove_items, results))
    t2 = threading.Thread(target=adder, args=(box, body.add_items, results))

    t1.start()
    t1.join()

    t2.start()
    t2.join()

    return results[::-1]

app.include_router(router, prefix="/api")

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)




