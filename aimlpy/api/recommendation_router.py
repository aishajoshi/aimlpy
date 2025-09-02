"""
-- Created by: Ashok Kumar Pant
-- Email: asokpant@gmail.com
-- Created on: 04/05/2025
"""
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from aimlpy.entity.recommendation_reqres import GetRecommendationRequest, GetRecommendationResponse
from aimlpy.service.recommendation_service import RecommendationService
from aimlpy.repo.datasource import get_db

router = APIRouter(prefix="/recommendations", tags=["recommendations"])


@router.post("", response_model=GetRecommendationResponse)
async def get_recommendations(
        request: GetRecommendationRequest,
        db: Session = Depends(get_db)
):
    """
    Get personalized recommendations for a user

    - **user_id**: ID of the user to get recommendations for
    - **top_k**: Number of recommendations to return (default: 10)
    """
    service = RecommendationService(db)
    response = await service.get_recommendations(request.user_id, request.top_k)

    if response.error:
        raise HTTPException(
            status_code=response.error_code.value,
            detail=response.message
        )

    return response


@router.get("/{user_id}", response_model=GetRecommendationResponse)
async def get_recommendations_by_id(
        user_id: str,
        top_k: int = 10,
        db: Session = Depends(get_db)
):
    """
    Get recommendations for a specific user ID

    - **user_id**: ID of the user to get recommendations for
    - **top_k**: Number of recommendations to return (default: 10)
    """
    service = RecommendationService(db)
    response = await service.get_recommendations(user_id, top_k)

    if response.error:
        raise HTTPException(
            status_code=response.error_code.value,
            detail=response.message
        )

    return response