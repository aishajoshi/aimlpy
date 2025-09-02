from datetime import datetime
from typing import Optional, Dict, Any
from pydantic import BaseModel, Field
from aimlpy.entity.common import BaseRequest, BaseResponse

class TrackActivityRequest(BaseRequest):
    user_id: str = Field(..., description="User ID performing the activity")
    activity_type: str = Field(..., description="Type of activity (view, click, purchase, etc.)")
    item_id: Optional[str] = Field(None, description="ID of the item interacted with")
    details: Optional[Dict[str, Any]] = Field(None, description="Additional activity details")
    duration: Optional[int] = Field(None, description="Duration of activity in seconds")
class ActivityResponse(BaseModel):
    activity_id: str = Field(..., description="Unique activity ID")
    user_id: str = Field(..., description="User ID")
    activity_type: str = Field(..., description="Type of activity")
    item_id: Optional[str] = Field(None, description="Item ID")
    timestamp: datetime = Field(..., description="When the activity occurred")

class TrackActivityResponse(BaseResponse):
    activity: Optional[ActivityResponse] = Field(None, description="Tracked activity details")

class UserActivityStatsResponse(BaseResponse):
    user_id: str = Field(..., description="User ID")
    total_activities: int = Field(..., description="Total number of activities")
    activity_types: Dict[str, int] = Field(..., description="Count by activity type")
    last_activity: Optional[datetime] = Field(None, description="Timestamp of last activity")