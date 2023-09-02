from fastapi import FastAPI 
import uvicorn 
from app.db.database import Base,engine
from fastapi.middleware.cors import CORSMiddleware
from app.routers import router_schedule
from app.routers import router_courses,router_professor

app = FastAPI()
app.include_router(router_schedule.router)
app.include_router(router_courses.router,prefix='/courses')
app.include_router(router_professor.router,prefix='/professor')


origins = ["*"]  # Esto permitirá cualquier origen

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

if __name__=="__main__":
    uvicorn.run("main:app",port=8000,reload=True)