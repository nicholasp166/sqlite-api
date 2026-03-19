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
    if os.listdir("database"):
        return os.listdir("database")
    else:
        return ["No DBs found"]


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

@app.post("/database/createTable/{dbName}")
async def createTable(dbName: str, body: TableRequest):
    with DBService(dbName) as dbs:
        dbs.addTable(body.name, body.obj)

    return RedirectResponse(url=f"/database/{dbName}", status_code=303)
  
@app.post("/database/createDatabase/{dbName}")
async def createDatabase(dbName: str):
    DBService.create(dbName)
    return RedirectResponse(url=f"/database/{dbName}", status_code=303)
  
@app.get("/database/{dbName}/{tableName}")
async def getTable(dbName: str, request: Request, tableName:str):
    try:
        with DBService(dbName) as dbs:
            tableSchema = tableSchema = dbs.executeSQL(f"PRAGMA table_info('{tableName}')")
        return templates.TemplateResponse("table.html", {
            "request":request,
            "table": tableSchema,
            "dbName":dbName
        })
    except Exception as e:
        return {"error": str(e)}
        #return RedirectResponse(url="/", status_code=303)

@app.get("/database/{dbName}")
async def getDatabase(dbName: str, request: Request):
    try:
        with DBService(dbName) as dbs:
            tables = dbs.getAlltables()
        return templates.TemplateResponse("database.html", {
            "request":request,
            "database": tables,
            "dbName": dbName
        })
    except:
        return RedirectResponse(url="/", status_code=303)


@app.get("/health")
async def health_check():
    return {"status": "ok"}