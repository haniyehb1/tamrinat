from fastapi import FastAPI, APIRouter, Body
import multiprocessing

app = FastAPI()
router = APIRouter()

# Function to calculate square of a number
def function_square(data):
    result = data * data
    return result

# Function to add 10 to a number
def add_ten(data):
    result = data + 10
    return result

# Function to get first character of a string
def first_char(data):
    return data[0]

# Function to count digits in an integer
def count_digits(number):
    return len(str(abs(number)))

# Route to handle scenario 18: Squaring numbers from 0 to 99
@router.post("/scenario-18", response_model=dict)
async def scenario_18():
    inputs = list(range(0, 100))
    pool = multiprocessing.Pool(processes=4)
    pool_outputs = pool.map(function_square, inputs)
    pool.close()
    pool.join()
    return {"scenario": 18, "output": pool_outputs}

# Route to handle scenario 28: Adding 10 to numbers from 0 to 9
@router.post("/scenario-28", response_model=dict)
async def scenario_28():
    inputs = list(range(0, 10))
    pool = multiprocessing.Pool(processes=5)
    pool_outputs = pool.map(add_ten, inputs)
    pool.close()
    pool.join()
    return {"scenario": 28, "output": pool_outputs}

# Route to handle scenario 38: Counting digits in a list of integers
@router.post("/scenario-38", response_model=dict)
async def scenario_38():
    inputs = [12345, 67890, 54321, 987654321, 123456789]
    pool = multiprocessing.Pool(processes=4)
    pool_outputs = pool.map(count_digits, inputs)
    pool.close()
    pool.join()
    return {"scenario": 38, "output": pool_outputs}

# Include the router in the main app
app.include_router(router, prefix="/api")

# Run the FastAPI application with Uvicorn server
if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)



