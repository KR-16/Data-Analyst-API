from fastapi import FastAPI, UploadFile, HTTPException
from fastapi.responses import JSONResponse
from fastapi.staticfiles import StaticFiles
from analyzer import DataAnalyser
import pandas as pd
from io import BytesIO

"""
FastAPI - web framework -  building APIs quickly - speed, simple, automatic documentation

WHY?
1. Fast - build on Starlette (async) and Pydantic (data validation)
2. Generates unteractive API docs
3. works with async/await for high performance
"""
app = FastAPI()
app.mount("/static", StaticFiles(directory = "app/static"), name = "static")

@app.get("/")
def root():
    return {"Message": "Data Analyst API Running"}

@app.post("/analyze")
#async - makes the function to pause/resume
#await - pauses the function until the task is completed
# Event loop - manages async tasks in background
async def analyze_data(file: UploadFile):
    try:
        # Read the file
        content = await file.read()
        if file.filename.endswith(".csv"):
            df = pd.read_csv(BytesIO(content))
        elif file.filename.endswith(".xlsx"):
            df = pd.read_excel(BytesIO(content))
        else:
            raise HTTPException(400, "Unsupported File Type")
        
        # Process Data
        cleaned_df = DataAnalyser.clean(df)
        analysis = DataAnalyser.analyze(cleaned_df)

        return JSONResponse(
            {
                "filename": file.filename,
                "columns": list(cleaned_df.columns),
                "analysis": analysis
            }
        )
    
    except Exception as e:
        raise HTTPException(500, f"Processing error: {str(e)}")
    
if __name__ == "__main__":
    import uvicorn
    # uvivorn - ASGI server to run the app
    # fastapi - core framework
    uvicorn.run(app, host="127.0.0.1", port=8000)