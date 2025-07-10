import uvicorn
from fastapi import FastAPI


app = FastAPI()


@app.get("/hello/")
def hello():
    return {
        "msg": "OK",
    }


if __name__ == "__main__":
    uvicorn.run("main:app", host="0.0.0.0", reload=True)
