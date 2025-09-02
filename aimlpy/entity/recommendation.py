"""
-- Created by: Ashok Kumar Pant
-- Email: asokpant@gmail.com
-- Created on: 04/05/2025
"""
from datetime import datetime
from typing import Optional
from pydantic import BaseModel, Field


class Recommendation(BaseModel):
    item_id: str = Field(..., description="The recommended item ID")
    score: float = Field(..., ge=0.0, le=1.0, description="Confidence score between 0-1")
    reason: Optional[str] = Field(None, description="Explanation for the recommendation")
    metadata: Optional[dict] = Field(default_factory=dict, description="Additional metadata")
    created_at: datetime = Field(default_factory=datetime.now, description="Creation timestamp")