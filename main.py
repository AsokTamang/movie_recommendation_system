import sys
sys.path.append('.')

import sys
from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles
from fastapi.responses import FileResponse
from utils import recommend_movies
import uvicorn
from fastapi.responses import JSONResponse

app = FastAPI()

app.mount('/static', StaticFiles(directory='statics'), name='statics')


@app.get('/')
def root():
    return FileResponse('statics/home.html')



@app.post('/recommend')
def predict(data:str): 
    try:
        movie_name = data

      
        result = recommend_movies(movie_name)
        return {'recommendation': result} 

    except Exception as e:
        return JSONResponse({"error": str(e)}, status_code=500)
    

if __name__=="__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000) 



