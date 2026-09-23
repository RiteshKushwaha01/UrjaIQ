from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app.database.database import get_db
from app.schemas.ai import AIChatRequest, AIChatResponse
from app.services.ai_service import generate_ai_response


router = APIRouter(
    prefix="/api/ai",
    tags=["AI Copilot"],
)


@router.post("/chat", response_model=AIChatResponse)
def chat(
    request: AIChatRequest,
    db: Session = Depends(get_db),
):
    try:
        answer = generate_ai_response(
            db,
            request.message,
        )

        return {
            "answer": answer
        }

    except Exception as error:
        raise HTTPException(
            status_code=500,
            detail=f"AI Copilot error: {str(error)}",
        )