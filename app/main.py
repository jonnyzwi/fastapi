
# https://www.youtube.com/watch?v=0sOvCWFmrtA&t=11h11m00s

# RUN IN TERMINAL TO START CONNECTION BETWEEN main.py AND SERVER
        # uvicorn app.main:app --reload
# ALSO CHECK TO MAKE SURE THAT BOTH THE INTERPRETER AND THE TERMINAL SHELL ARE IN VIRTUAL ENVIRONMENT venv

from app import database
from .masterImports import *
from .routers import basicPosts, postgres, sqlalchemy, user, auth, logins, vote, current_user
from .config import settings
from fastapi.middleware.cors import CORSMiddleware 


models.Base.metadata.create_all(bind=engine)

app = FastAPI()

origins = ['*'] #["https://www.google.com"]

app.add_middleware(
        CORSMiddleware,
        allow_origins=origins,
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
)

app.include_router(basicPosts.router)
app.include_router(postgres.router)
app.include_router(sqlalchemy.router)
app.include_router(user.router)
app.include_router(auth.router)
app.include_router(logins.router)
app.include_router(vote.router)
app.include_router(current_user.router)
