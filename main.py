import os
import json
import requests
import fal_client
from dotenv import load_dotenv
from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware

load_dotenv()
app = FastAPI(
    title="RocketTools",
    description="RocketTools' Image Generator",
    docs_url="/docs",
    version="v1",
)

origins = ["*"]
app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
FAL_API_KEY = os.getenv('FAL_API')

async def img_webhook_ap(output_data):
     ap_webhook_url = "https://cloud.activepieces.com/api/v1/webhooks/uknq9Me5dinKhI7h0ipjJ"
     res = requests.post(ap_webhook_url, data=json.dumps(output_data),headers={'Content-Type': 'application/json'})
     return

async def submit(user_prompt: str):
    try:
        handler = await fal_client.submit_async(
            "fal-ai/flux/schnell",
            arguments={"prompt": user_prompt},
        )

        log_index = 0
        async for event in handler.iter_events(with_logs=True):
            if isinstance(event, fal_client.InProgress):
                new_logs = event.logs[log_index:]
                for log in new_logs:
                    print(log["message"])
                log_index = len(event.logs)

        result = await handler.get()
        if 'images' not in result or not result['images']:
            raise HTTPException(status_code=500, detail="No images returned from the API")

        return {"image_url": result['images'][0]['url']}
    
    except fal_client.FalClientError:
        raise HTTPException(status_code=500, detail="Failed to communicate with the image generation service")
    except Exception:
        raise HTTPException(status_code=500, detail="An unexpected error occurred")

@app.get("/")
def fluxai():
    return {"message": "Welcome to FluxAI"}

@app.post("/prompt/{user_prompt}")
async def image_prompt(user_prompt: str):
    try:
        img_url = await submit(user_prompt) 
        await img_webhook_ap(img_url)
        return {"image_url": img_url}
    except HTTPException as e:
        raise e
    except Exception:
        raise HTTPException(status_code=500, detail="An unexpected error occurred")

if __name__ == "__main__":
    import uvicorn
    uvicorn.run("main:app", host="0.0.0.0", port=8000, reload=True)
