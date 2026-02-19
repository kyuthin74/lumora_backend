from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List

from app.api.auth import get_current_user
from app.database import get_db
from app.schemas.depression_risk_result import (
    DepressionRiskResultCreate,
    DepressionRiskResultResponse,
)
from app.crud.depression_risk_result import (
    create_risk_result,
    get_risk_results_by_user,
)
from app.crud.depression_test import get_depression_test_by_id
from app.services.prediction_service import prediction_service

router = APIRouter(
    prefix="/depression-risk-results",
    tags=["Depression Risk Results"],
)


@router.post(
    "",
    response_model=DepressionRiskResultResponse,
    status_code=201,
)
def create_depression_risk_result(
    result: DepressionRiskResultCreate,
    current_user=Depends(get_current_user),
    db: Session = Depends(get_db),
):
    if current_user.id != result.user_id:
        raise HTTPException(
            status_code=403,
            detail="You do not have permission to create a risk result for this user"
        )
    return create_risk_result(
        db=db,
        user_id=result.user_id,
        depression_test_id=result.depression_test_id,
        risk_level=result.risk_level,
        risk_score=result.risk_score,
    )


@router.post(
    "/predict/{depression_test_id}",
    response_model=DepressionRiskResultResponse,
    status_code=201,
)
def predict_and_save_risk_result(
    depression_test_id: int,
    current_user=Depends(get_current_user),
    db: Session = Depends(get_db),
):
    """
    Run ML model prediction on a depression test and save the result.
    
    Args:
        depression_test_id: ID of the depression test to analyze
        db: Database session
        
    Returns:
        The created depression risk result with predictions
    """
    # Get the depression test data
    test = get_depression_test_by_id(db, depression_test_id)
    if not test:
        raise HTTPException(
            status_code=404,
            detail=f"Depression test with ID {depression_test_id} not found"
        )
    
    # Check if current user has permission to access this test
    if current_user.id != test.user_id:
        raise HTTPException(
            status_code=403,
            detail="You do not have permission to access this depression test"
        )
    
    # Convert test data to dictionary for prediction
    test_data = {
        'mood': test.mood,
        'sleep_hour': test.sleep_hour,
        'appetite': test.appetite,
        'exercise': test.exercise,
        'screen_time': test.screen_time,
        'academic_work': test.academic_work,
        'socialize': test.socialize,
        'energy_level': test.energy_level,
        'trouble_concentrating': test.trouble_concentrating,
        'negative_thoughts': test.negative_thoughts,
        'decision_making': test.decision_making,
        'bothered_things': test.bothered_things,
        'sleepy_tired': test.sleepy_tired,
        'stressful_events': test.stressful_events,
        'future_hope': test.future_hope,
    }
    
    # Run prediction
    try:
        risk_score, risk_level = prediction_service.predict_depression_risk(test_data)
    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=f"Prediction failed: {str(e)}"
        )
    
    # Save result to database
    result = create_risk_result(
        db=db,
        user_id=test.user_id,
        depression_test_id=depression_test_id,
        risk_level=risk_level,
        risk_score=risk_score,
    )
    
    return result


# @router.get(
#     "/{result_id}",
#     response_model=DepressionRiskResultResponse,
# )
# def read_risk_result(result_id: int, db: Session = Depends(get_db)):
#     result = get_risk_result_by_id(db, result_id)
#     if not result:
#         raise HTTPException(status_code=404, detail="Risk result not found")
#     return result


@router.get(
    "",
    response_model=List[DepressionRiskResultResponse],
)
def read_user_risk_results(user_id: int, current_user=Depends(get_current_user), db: Session = Depends(get_db)):
    if current_user.id != user_id:
        raise HTTPException(
            status_code=403,
            detail="You do not have permission to access risk results for this user"
        )
    return get_risk_results_by_user(db, user_id)

