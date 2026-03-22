from fastapi import FastAPI

app = FastAPI()

@app.get("/")
def read_root():
    return {"message": "Intelligent Monitoring System Running 🚀"}

@app.get("/health")
def health_check():
    return {"status": "OK"}