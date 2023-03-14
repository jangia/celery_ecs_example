from fastapi import FastAPI
from fastapi.responses import JSONResponse

import celery_app

app = FastAPI()


@app.get("/send-newsletter")
def send_newsletter():
    task = celery_app.send_newsletter.apply_async()
    return JSONResponse({"task_id": task.id})


@app.get("/send-newsletter/fan-out")
def send_newsletter_fanout():
    task = celery_app.send_newsletter_fan_out.apply_async()
    return JSONResponse({"task_id": task.id})


@app.get("/send-newsletter/batching")
def send_newsletter_fanout():
    task = celery_app.send_newsletter_batching.apply_async()
    return JSONResponse({"task_id": task.id})