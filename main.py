import sys

sys.path.append(".")
import pickle
import sys
from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles
from fastapi.responses import FileResponse
from utils import recommend_movies
import uvicorn
from pydantic import BaseModel
from fastapi.responses import JSONResponse
from fastapi import FastAPI

app = FastAPI()

app.mount("/static", StaticFiles(directory="statics"), name="statics")




class RecommendRequest(BaseModel):
    data: str

@app.get("/")
def root():
    return FileResponse("statics/home.html")


# this endpoint returns all the available movie list
@app.get("/movies")
def get_movies():
    movies = pickle.load(open("artifacts/movie_df.pkl", "rb"))
    return {"movies": movies["title"].tolist()}


@app.post("/recommend")
def predict(request: RecommendRequest):
    try:
        movie_name =request.data

        result = recommend_movies(movie_name)
        return {"recommendation": result}

    except IndexError:
        return JSONResponse(
            {"error": f"Movie '{movie_name}' not found in database."}, status_code=404
        )
    except KeyError as e:
        return JSONResponse({"error": f"Missing column: {str(e)}"}, status_code=500)
    except Exception as e:
        return JSONResponse({"error": str(e)}, status_code=500)


if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)



