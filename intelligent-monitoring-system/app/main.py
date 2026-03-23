from fastapi import FastAPI
from core.config import APP_NAME
import logging
from core.logging_config import setup_logging
import random
import time
setup_logging()
logger = logging.getLogger(__name__)

app = FastAPI()


logger.info(f"Starting {APP_NAME}")
@app.get("/")
def read_root():
    logger.info("Root endpoint called")
    return {"message": "Intelligent Monitoring System Running 🚀"}

@app.get("/health")
def health_check():
    logger.info("Health check endpoint hit")
    return {"status": "OK"}



@app.get("/simulate")
def simulate_load():
    delay = random.uniform(0.1, 1.5)
    time.sleep(delay)

    if random.random() < 0.2:
        logger.error("Simulated failure occurred")
        return {"status": "error", "message": "Something went wrong"}

    logger.info(f"Request processed in {delay:.2f} seconds")
    return {"status": "success", "response_time": delay}