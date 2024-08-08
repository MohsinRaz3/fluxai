import os
import asyncio
from fluxai import submit
from dotenv import load_dotenv
from fastapi import FastAPI

load_dotenv()
FAL_API_KEY = os.getenv('FAL_API')

app = FastAPI(title="FLux.ai", docs_url="/docs")

@app.get("/")
def fluxai():
    return {"message" : "welcome to fluxai"}
@app.post("/prompt")
async def image_prompt(prompt:str):
     img_url =  await submit(prompt)
     return {"image_url":img_url}
 
 
if __name__ == "__main__":
    import uvicorn
    uvicorn.run("main:app", host="0.0.0.0", port=8000, reload=True)