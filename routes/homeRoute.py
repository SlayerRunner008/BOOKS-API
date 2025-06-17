from fastapi import APIRouter

router = APIRouter()

@router.get("/", tags=["Home"])
def message():
    return {"message": "Prueba de pipeline de CI/CD con FastAPI y GitHub Actions"}