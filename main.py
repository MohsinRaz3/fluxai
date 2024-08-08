import os
from fluxai import submit
import asyncio
from dotenv import load_dotenv
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

load_dotenv()

app = FastAPI(
    title="RocketTools",
    description="RocketTools' Image genenator",
    docs_url="/docs",
    version="v1",
)

origins = [
    "https://typebot.co/mohsinraz",
    "https://typebot.co/",
    "https://fluxai.onrender.com/",
    "https://fluxai.onrender.com/prompt",
    "https://salad-api-v2.onrender.com",
    "https://salad-api-v2.onrender.com/",
    "https://salad-api-v2.onrender.com/transcribe"
    "https://web.postman.co/",
    "https://rocket-tools.netlify.app",
    "https://salad-api.vercel.app/",
    "https://salad-api.vercel.app/transcribe",
    "https://salad-api.vercel.app",
    "http://localhost:3000/",
    "http://localhost:3000",
    "http://127.0.0.1:3000",
    "http://127.0.0.1:8000/",
    "http://localhost:3001/",
    "http://localhost",
    "http://localhost:8000/",
    "http://localhost:8000",
    "http://127.0.0.1:8000",
    "http://127.0.0.1:3000/",
    "http://localhost",
    "http://localhost:8000",
    "http://localhost:3000",
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
FAL_API_KEY = os.getenv('FAL_API')

app = FastAPI(title="FLux.ai", docs_url="/docs")

@app.get("/")
def fluxai():
    return {"message" : "welcome to fluxai"}

@app.post("/prompt/{user_prompt}")
async def image_prompt(user_prompt:str):
     img_url = await asyncio.create_task(submit(user_prompt))
     return {"image_url":img_url}
 
 
if __name__ == "__main__":
    import uvicorn
    uvicorn.run("main:app", host="0.0.0.0", port=8000, reload=True)