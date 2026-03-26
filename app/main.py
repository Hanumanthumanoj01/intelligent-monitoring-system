from fastapi import FastAPI
import logging
import random
import time

from core.logging_config import setup_logging
from core.redis_client import redis_client

setup_logging()
logger = logging.getLogger(__name__)

app = FastAPI()

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