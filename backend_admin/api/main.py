from app import create_app

app = create_app()

@app.get("/")
async def root():
    return {"message": "后台管理系统API", "version": "1.0.0"}

if __name__ == "__main__":
    import uvicorn
    uvicorn.run("main:app", host="0.0.0.0", port=13286, reload=True)
