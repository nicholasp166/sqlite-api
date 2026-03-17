from fastapi import FastAPI, Request #type: ignore
from fastapi.templating import Jinja2Templates # type: ignore
from fastapi.responses import RedirectResponse # type: ignore
import os
from services import DBService
from pydantic import BaseModel #type: ignore

class TableRequest(BaseModel):
    name: str
    obj: list[str]



def showDB():
    return os.listdir("database")


app = FastAPI()
templates = Jinja2Templates(directory="templates")

# main.py
@app.get("/")
async def index(request: Request):
    return templates.TemplateResponse("index.html", {
        "request": request,
        "message": "Hello World",
        "databases": showDB(),
    })

@app.post("/databases/createTable/{dbName}")
async def createTable(dbName: str, body: TableRequest):
    with DBService(dbName) as dbs:
        dbs.addTable(body.name, body.obj)

    return RedirectResponse(url=f"/databases/{dbName}", status_code=303)
  

@app.get("/databases/{dbName}")
async def getDatabase(dbName: str, request: Request):
    with DBService(dbName) as dbs:
        tables = dbs.getAlltables()
  
    return templates.TemplateResponse("database.html", {
        "request":request,
        "database": tables
    })

@app.get("/health")
async def health_check():
    return {"status": "ok"}