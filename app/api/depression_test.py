from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from typing import List

from app.api.auth import get_current_user
from app.database import get_db
from app.schemas.depression_risk_result import DepressionRiskResultResponse
from app.schemas.depression_test import (
    DepressionTestCreate,
    DepressionTestResponse,
)
from app.crud.depression_test import (
    create_depression_test,
    get_depression_test_by_id,
    get_depression_tests_by_user,
)

router = APIRouter(
    prefix="/depression-test",
    tags=["Depression Test"],
)


@router.post(
    "",
    response_model=DepressionRiskResultResponse,
    status_code=status.HTTP_201_CREATED,
)
def create_test(
    depression_test: DepressionTestCreate,
    current_user=Depends(get_current_user),
    db: Session = Depends(get_db),
):
    if current_user.id != depression_test.user_id:
        raise HTTPException(
            status_code=403,
            detail="You do not have permission to create a depression test for this user"
        )
    return create_depression_test(db, depression_test)


# @router.get(
#     "/{test_id}",
#     response_model=DepressionTestResponse,
# )
# def read_test(test_id: int, current_user=Depends(get_current_user), db: Session = Depends(get_db)):
#     test = get_depression_test_by_id(db, test_id)
#     if not test:
#         raise HTTPException(status_code=404, detail="Depression test not found")
#     if current_user.id != test.user_id:
#         raise HTTPException(
#             status_code=403,
#             detail="You do not have permission to access this depression test"
#         )
#         raise HTTPException(status_code=404, detail="Depression test not found")
#     return test


# @router.get(
#     "",
#     response_model=List[DepressionTestResponse],
# )
# def read_user_tests(user_id: int, current_user=Depends(get_current_user), db: Session = Depends(get_db)):
#     if current_user.id != user_id:
#         raise HTTPException(
#             status_code=403,
#             detail="You do not have permission to access tests for this user"
#         )
#     return get_depression_tests_by_user(db, user_id)
