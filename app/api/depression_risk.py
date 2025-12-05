from fastapi import APIRouter, Depends, HTTPException, status, Query
from sqlalchemy.orm import Session
from typing import List, Optional
from app.database import get_db
from app.models.depression_risk import (
    DepressionRiskInput,
    DepressionRiskResult,
    DepressionRiskResponse,
    RiskTrend
)
from app.crud import depression_risk_result as risk_crud
from app.ml.prediction import predict_depression_risk
from app.api.auth import get_current_user
from app.services.alert_service import process_risk_alert

router = APIRouter(prefix="/risk", tags=["Depression Risk"])


@router.post("/predict", response_model=DepressionRiskResult)
async def predict_risk(
    risk_input: DepressionRiskInput,
    current_user = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """Predict depression risk based on input data"""
    # Make prediction
    result = predict_depression_risk(risk_input)
    
    # Save result to database
    input_data = risk_input.model_dump()
    db_risk = risk_crud.create_risk_result(
        db=db,
        user_id=current_user.id,
        risk_level=result.risk_level,
        risk_score=result.risk_score,
        input_data=input_data
    )
    
    # Process alert if risk is high
    try:
        await process_risk_alert(
            db=db,
            user=current_user,
            risk_level=result.risk_level,
            risk_score=result.risk_score,
            recommendation=result.recommendation
        )
    except Exception as e:
        print(f"Alert processing failed: {e}")
    
    return result


@router.get("/history", response_model=List[DepressionRiskResponse])
async def get_risk_history(
    skip: int = Query(0, ge=0),
    limit: int = Query(50, ge=1, le=500),
    days: Optional[int] = Query(None, ge=1, le=365),
    current_user = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """Get risk assessment history"""
    results = risk_crud.get_user_risk_results(
        db,
        user_id=current_user.id,
        skip=skip,
        limit=limit,
        days=days
    )
    return results


@router.get("/history/{risk_id}", response_model=DepressionRiskResponse)
async def get_risk_result(
    risk_id: int,
    current_user = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """Get a specific risk result"""
    result = risk_crud.get_risk_result_by_id(db, risk_id=risk_id, user_id=current_user.id)
    
    if not result:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Risk result not found"
        )
    
    return result


@router.get("/latest", response_model=DepressionRiskResponse)
async def get_latest_risk(
    current_user = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """Get the most recent risk assessment"""
    result = risk_crud.get_latest_risk_result(db, user_id=current_user.id)
    
    if not result:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="No risk assessments found"
        )
    
    return result


@router.get("/trend", response_model=RiskTrend)
async def get_risk_trend(
    days: int = Query(30, ge=1, le=365),
    current_user = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """Get risk trend analysis"""
    trend = risk_crud.get_risk_trend(db, user_id=current_user.id, days=days)
    return RiskTrend(**trend)
