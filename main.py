
# from pathlib import Path

# from fastapi import FastAPI, HTTPException
# from fastapi.responses import FileResponse
# from pydantic import BaseModel

# from graph import sql_agent
# from schema_inspector import get_database_schema

# BASE_DIR = Path(__file__).resolve().parent

# app = FastAPI(
#     title="AI SQL Agent",
#     description="Natural Language to SQL using LangGraph and Groq",
#     version="1.0.0"
# )


# class QuestionRequest(BaseModel):
#     question: str


# @app.get("/")
# def home():
#     return FileResponse(BASE_DIR / "index.html")


# @app.get("/style.css")
# def get_css():
#     return FileResponse(BASE_DIR / "style.css")


# @app.get("/script.js")
# def get_js():
#     return FileResponse(BASE_DIR / "script.js")


# @app.get("/api/schema")
# def database_schema():
#     try:
#         schema = get_database_schema()
#         return {"schema": schema}
#     except Exception as error:
#         raise HTTPException(status_code=500, detail=str(error))


# @app.post("/api/generate-sql")
# def generate_sql(request: QuestionRequest):
#     if not request.question.strip():
#         raise HTTPException(
#             status_code=400,
#             detail="Please enter a question."
#         )

#     try:
#         result = sql_agent.invoke({
#             "question": request.question
#         })

#         return {
#             "question": request.question,
#             "sql": result.get("sql", ""),
#             "is_valid": result.get("is_valid", False),
#             "validation_error": result.get("validation_error", None)
#         }

#     except Exception as error:
#         raise HTTPException(
#             status_code=500,
#             detail=str(error)
#         )


from pathlib import Path

from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import FileResponse
from pydantic import BaseModel

from graph import sql_agent
from schema_inspector import get_database_schema

BASE_DIR = Path(__file__).resolve().parent

app = FastAPI(
    title="AI SQL Agent",
    description="Natural Language to SQL using LangGraph and Groq",
    version="1.0.0"
)

# CORS configuration for VS Code Live Server
app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "http://127.0.0.1:5500",
        "http://localhost:5500",
        "http://127.0.0.1:5501",
        "http://localhost:5501"
    ],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


class QuestionRequest(BaseModel):
    question: str


@app.get("/")
def home():
    return FileResponse(BASE_DIR / "index.html")


@app.get("/style.css")
def get_css():
    return FileResponse(BASE_DIR / "style.css")


@app.get("/script.js")
def get_js():
    return FileResponse(BASE_DIR / "script.js")


@app.get("/api/schema")
def database_schema():
    try:
        schema = get_database_schema()
        return {"schema": schema}
    except Exception as error:
        raise HTTPException(
            status_code=500,
            detail=str(error)
        )


@app.post("/api/generate-sql")
def generate_sql(request: QuestionRequest):
    if not request.question.strip():
        raise HTTPException(
            status_code=400,
            detail="Please enter a question."
        )

    try:
        result = sql_agent.invoke({
            "question": request.question
        })

        return {
            "question": request.question,
            "sql": result.get("sql", ""),
            "is_valid": result.get("is_valid", False),
            "validation_error": result.get("validation_error", None)
        }

    except Exception as error:
        raise HTTPException(
            status_code=500,
            detail=str(error)
        )
