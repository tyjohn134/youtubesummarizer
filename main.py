from fastapi import FastAPI
from celery import Celery
from model import SummarizeRequest
from celery_worker import create_summarization

# Create FastAPI app
app = FastAPI()
# Create request endpoint
celery = Celery('tasks', broker='amqp://guest:guest@127.0.0.1:5672//',
                backend="redis://localhost:6379/0")


@app.post('/summarize')
def request_summarization(request: SummarizeRequest):
    # use delay() method to call the celery task
    req_id = create_summarization.delay(request.url)

    return {"message": "Summarization Request Received!", "requestid": str(req_id)}


@app.get("/tasks/{task_id}")
def get_status(task_id):
    task_result = celery.AsyncResult(task_id)
    result = {
        "task_id": task_id,
        "task_status": task_result.status,
        "task_result": task_result.result
    }
    return result
