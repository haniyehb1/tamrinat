from fastapi import FastAPI
from fastapi.routing import APIRouter
from tamrin1_1 import router as tamrin1_1_router
from tamrin2_1 import router as tamrin2_1_router
from tamrin3_1 import router as tamrin3_1_router
from tamrin4_1 import router as tamrin4_1_router
from tamrin5_1 import router as tamrin5_1_router
from tamrin6_1 import router as tamrin6_1_router
from tamrin7_1 import router as tamrin7_1_router
from tamrinone_2 import router as tamrinone_2_router
from tamrintwo_2 import router as tamrintwo_2_router
from tamrintree_2 import router as tamrintree_2_router
from tamrinfour_2 import router as tamrinfour_2_router
from tamrinfive_2 import router as tamrinfive_2_router
from tamrinsix_2 import router as tamrinsix_2_router
from tamrinseven_2 import router as tamrinseven_2_router
from tamrineight_2 import router as tamrineight_2_router

app = FastAPI()

app.include_router(tamrin1_1_router, tags=["tamrin1_1"])
app.include_router(tamrin2_1_router, tags=["tamrin2_1"])
app.include_router(tamrin3_1_router, tags=["tamrin3_1"])
app.include_router(tamrin4_1_router, tags=["tamrin4_1"])
app.include_router(tamrin5_1_router, prefix="/api", tags=["tamrin5_1"])
app.include_router(tamrin6_1_router, tags=["tamrin6_1"])
app.include_router(tamrin7_1_router, tags=["tamrin7_1"])
app.include_router(tamrinone_2_router, prefix="/api", tags=["tamrinone_2"])
app.include_router(tamrintwo_2_router, tags=["tamrintwo_2"])
app.include_router(tamrintree_2_router, tags=["tamrintree_2"])
app.include_router(tamrinfour_2_router, tags=["tamrinfour_2"])
app.include_router(tamrinfive_2_router, tags=["tamrinfive_2"])
app.include_router(tamrinsix_2_router, tags=["tamrinsix_2"])
app.include_router(tamrinseven_2_router, tags=["tamrinseven_2"])
app.include_router(tamrineight_2_router, prefix="/api", tags=["tamrineight_2"])

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)







