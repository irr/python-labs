from fastapi import FastAPI

app = FastAPI()

@app.get("/")
async def root():
    return {"message": "Test OK"}

# run with:
# - uvicorn main:app --reload (dev)
# - uvicorn main:app (production)
