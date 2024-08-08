import os
import asyncio
import fal_client
from dotenv import load_dotenv
from fastapi import FastAPI

app = FastAPI(title="FLux.ai", docs_url="/docs")

load_dotenv()
FAL_API_KEY = os.getenv('FAL_API')

@app.post("/prompt")
async def submit(art_prompt: str):
    handler = await fal_client.submit_async(
        "fal-ai/flux/schnell",
        arguments={
            "prompt": f"{art_prompt}"
        },
    )

    log_index = 0
    async for event in handler.iter_events(with_logs=True):
        if isinstance(event, fal_client.InProgress):
            new_logs = event.logs[log_index:]
            for log in new_logs:
                print(log["message"])
            log_index = len(event.logs)

    result = await handler.get()
    print(result)


if __name__ == "__main__":
    asyncio.run(submit())