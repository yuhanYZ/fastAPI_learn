# the first code about fastapi
from fastapi import FastAPI
import uvicorn

app =FastAPI()


@app.get("/")
def read_root():
    return {'Hello':'World111'}

@app.get("/items/{item_id}")
def read_item(item_id: int):
    return {'item_id': item_id}

if __name__=='__main__':
    uvicorn.run("main01:app", host='127.0.0.1', port=8000,reload=True)