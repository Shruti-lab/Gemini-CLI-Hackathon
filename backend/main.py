from fastapi import FastAPI
from backend.routes import upload, compare, ask

app = FastAPI(title="Excel AI Version Control System")

# Include routes
app.include_router(upload.router)
app.include_router(compare.router)
app.include_router(ask.router)

@app.get("/health")
async def health_check():
    return {"status": "ok", "message": "Excel AI VCS is ready"}

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
