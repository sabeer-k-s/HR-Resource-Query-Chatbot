# src/api/routes.py
from fastapi import FastAPI, HTTPException, Depends
from pydantic import BaseModel
from typing import List
from ..data.data_loader import load_employees
from ..rag.retriever import Retriever
from ..rag.generator import Generator
from ..rag.embeddings import EmbeddingsManager

class QueryRequest(BaseModel):
    query: str

class Employee(BaseModel):
    id: int
    name: str
    skills: List[str]
    experience_years: int
    projects: List[str]
    availability: str

def get_retriever():
    """Dependency to provide Retriever instance."""
    employees = load_employees("data/employees.json")
    embeddings_manager = EmbeddingsManager()
    return Retriever(employees, embeddings_manager)

def get_generator():
    """Dependency to provide Generator instance."""
    return Generator()

def create_app() -> FastAPI:
    app = FastAPI(title="HR Resource Query Chatbot")

    @app.get("/employees/search", response_model=List[Employee])
    async def search_employees(skills: str = None, min_experience: int = 0):
        try:
            employees = load_employees("data/employees.json")
            filtered_employees = employees
            if skills:
                skills_list = [s.strip().lower() for s in skills.split(",")]
                filtered_employees = [
                    emp for emp in filtered_employees
                    if any(skill in [s.lower() for s in emp["skills"]] for skill in skills_list)
                ]
            filtered_employees = [
                emp for emp in filtered_employees
                if emp["experience_years"] >= min_experience
            ]
            return filtered_employees
        except Exception as e:
            raise HTTPException(status_code=500, detail=str(e))

    @app.post("/chat")
    async def chat_query(request: QueryRequest, retriever: Retriever = Depends(get_retriever), generator: Generator = Depends(get_generator)):
        try:
            matched_employees = retriever.retrieve(request.query)
            response = generator.generate_response(request.query, matched_employees)
            return {"response": response}
        except Exception as e:
            raise HTTPException(status_code=500, detail=str(e))

    return app