from fastapi import FastAPI, Request
from logging_config import logger
from monitoring import REQUEST_COUNT, REQUEST_LATENCY, registry
from slowapi.errors import RateLimitExceeded
from slowapi.middleware import SlowAPIMiddleware
from slowapi.util import get_remote_address
from slowapi import Limiter, _rate_limit_exceeded_handler
from prometheus_client import generate_latest
import time

app = FastAPI()

# ---------------------------
#  RATE LIMIT CONFIG (Number 4)
# ---------------------------
app.state.limiter = Limiter(key_func=get_remote_address)
app.add_exception_handler(RateLimitExceeded, _rate_limit_exceeded_handler)
app.add_middleware(SlowAPIMiddleware)

# ---------------------------
#  MONITORING MIDDLEWARE
# ---------------------------
@app.middleware("http")
async def metrics_middleware(request: Request, call_next):
    start = time.time()
    response = await call_next(request)
    duration = time.time() - start

    REQUEST_LATENCY.labels(request.url.path).observe(duration)
    REQUEST_COUNT.labels(
        request.method, request.url.path, response.status_code
    ).inc()

    logger.info(f"{request.method} {request.url.path} {response.status_code}")
    return response

# ---------------------------
#  API ENDPOINT uvicorn main:app --reload --port 3000
# ---------------------------
from fastapi import Request

@app.get("/hello")
@app.state.limiter.limit("5/minute")
def hello(request: Request):
    return {"message": "Hello Service Operation with Python!"}


@app.get("/metrics")
def metrics():
    return generate_latest(registry)
