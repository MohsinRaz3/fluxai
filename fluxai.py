import fal_client

async def submit(prompt: str):
    handler = await fal_client.submit_async(
        "fal-ai/flux/schnell",
        arguments={
            "prompt": f"{prompt}"
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
    return result['images'][0]['url']

