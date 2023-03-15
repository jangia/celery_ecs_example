from fastapi import FastAPI, Request
from fastapi.responses import HTMLResponse, JSONResponse

import celery_app

app = FastAPI()


@app.get("/")
def home(request: Request):
    return HTMLResponse(
        f"""
        <html>
        <head>
        <title>Celery on AWS ECS examples</title>
        </head>
        <body>
        <div><a href="{request.url_for('send_newsletter')}">Send newsletter - Single Job</a></div>
        <div><a href="{request.url_for('send_newsletter_fanout')}">Send newsletter - Fan-out</a></div>
        <div><a href="{request.url_for('send_newsletter_batching')}">Send newsletter - Batching</a></div>
        <div><a href="{request.url_for('send_newsletter_locking')}">Send newsletter - Locking</a></div>
        </body>
        </html>
        """
    )


@app.get("/send-newsletter")
def send_newsletter():
    task = celery_app.send_newsletter.apply_async()
    return JSONResponse({"task_id": task.id})


@app.get("/send-newsletter/fan-out")
def send_newsletter_fanout():
    task = celery_app.send_newsletter_fan_out.apply_async()
    return JSONResponse({"task_id": task.id})


@app.get("/send-newsletter/batching")
def send_newsletter_batching():
    task = celery_app.send_newsletter_batching.apply_async()
    return JSONResponse({"task_id": task.id})


@app.get("/send-newsletter/locking")
def send_newsletter_locking():
    task = celery_app.send_newsletter_locking.apply_async()
    return JSONResponse({"task_id": task.id})
