from fastapi import FastAPI
from backend.routes import upload, compare, insights, ask_v1, analyse

app = FastAPI(title="Excel AI Version Control System")

# Core routes (Used by CLI and general operations)
app.include_router(upload.router)
app.include_router(compare.router)

# v1 routes (Required for Karate tests and AI insights)
app.include_router(insights.router)
app.include_router(ask_v1.router)
app.include_router(analyse.router)

@app.get("/health")
async def health_check():
    return {"status": "ok", "message": "Excel AI VCS is ready"}

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
