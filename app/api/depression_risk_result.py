from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List

from app.database import get_db
from app.schemas.depression_risk_result import DepressionRiskResultResponse
from app.crud.depression_risk_result import (
    get_risk_result_by_id,
    get_risk_results_by_user,
    get_latest_risk_result_by_user,
)

router = APIRouter(
    prefix="/depression-risk-results",
    tags=["Depression Risk Results"],
)


@router.get(
    "/{result_id}",
    response_model=DepressionRiskResultResponse,
)
def read_risk_result(result_id: int, db: Session = Depends(get_db)):
    result = get_risk_result_by_id(db, result_id)
    if not result:
        raise HTTPException(status_code=404, detail="Risk result not found")
    return result


@router.get(
    "",
    response_model=List[DepressionRiskResultResponse],
)
def read_user_risk_results(user_id: int, db: Session = Depends(get_db)):
    return get_risk_results_by_user(db, user_id)


@router.get(
    "/{user_id}/latest",
    response_model=DepressionRiskResultResponse,
)
def read_latest_risk_result(user_id: int, db: Session = Depends(get_db)):
    result = get_latest_risk_result_by_user(db, user_id)
    if not result:
        raise HTTPException(
            status_code=404,
            detail="No risk results found for this user",
        )
    return result
