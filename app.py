from fastapi import FastAPI
import uvicorn

app = FastAPI()

# defining endpoints
@app.get("/")
def homepage():
    return "WELCOME TO FASTAPI"

@app.get("/hello/{name}")
def homepage(name):
    return f"Hello user {name}"



if __name__=="__main__":
    uvicorn.run("app:app")