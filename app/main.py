from fastapi import FastAPI, Request
from fastapi.responses import Response

import logging
import random
import time

from prometheus_client import generate_latest

from core.metrics import REQUEST_COUNT, REQUEST_LATENCY
from core.logging_config import setup_logging
from core.redis_client import redis_client

# Setup logging
setup_logging()
logger = logging.getLogger(__name__)

app = FastAPI()


# -----------------------
# Middleware (Metrics)
# -----------------------
@app.middleware("http")
async def metrics_middleware(request: Request, call_next):
    start_time = time.time()

    response = await call_next(request)

    duration = time.time() - start_time

    REQUEST_COUNT.inc()
    REQUEST_LATENCY.observe(duration)

    return response


# -----------------------
# Routes
# -----------------------
@app.get("/")
def read_root():
    logger.info("Root endpoint called")
    return {"message": "Intelligent Monitoring System Running 🚀"}


@app.get("/health")
def health_check():
    return {"status": "OK"}


@app.get("/cache")
def cache_data():
    value = random.randint(1, 100)
    redis_client.set("random_value", value)

    logger.info(f"Stored value in Redis: {value}")
    return {"stored_value": value}


@app.get("/get-cache")
def get_cache():
    value = redis_client.get("random_value")

    logger.info(f"Retrieved value from Redis: {value}")
    return {"cached_value": value}


@app.get("/simulate")
def simulate_load():
    delay = random.uniform(0.1, 1.5)
    time.sleep(delay)

    if random.random() < 0.2:
        logger.error("Simulated failure occurred")
        return {"status": "error", "message": "Something went wrong"}

    logger.info(f"Request processed in {delay:.2f} seconds")
    return {"status": "success", "response_time": delay}


# -----------------------
# Metrics Endpoint
# -----------------------
@app.get("/metrics")
def metrics():
    return Response(generate_latest(), media_type="text/plain")