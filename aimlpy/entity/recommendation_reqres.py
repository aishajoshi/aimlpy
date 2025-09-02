"""
-- Created by: Ashok Kumar Pant
-- Email: asokpant@gmail.com
-- Created on: 04/05/2025
"""
from datetime import datetime
from typing import List, Optional
from pydantic import Field
from aimlpy.entity.common import BaseRequest, BaseResponse, Pagination
from aimlpy.entity.recommendation import Recommendation


class GetRecommendationRequest(BaseRequest):
    user_id: str = None
    top_k: int = 10


class GetRecommendationResponse(BaseResponse):
    user_id: str = Field(..., description="The user ID recommendations are for")
    recommendations: List[Recommendation] = Field(..., description="List of recommendations")
    total_count: int = Field(..., description="Total number of recommendations")
    generated_at: datetime = Field(default_factory=datetime.now, description="Timestamp of generation")
    pagination: Optional[Pagination] = Field(None, description="Pagination information")

    class Config:
        json_encoders = {
            datetime: lambda v: v.isoformat()
        }