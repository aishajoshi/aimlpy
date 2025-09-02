"""
-- Created by: Ashok Kumar Pant
-- Email: asokpant@gmail.com
-- Created on: 04/05/2025
"""
from sqlalchemy import Column, String, Text, ForeignKey, Integer
from sqlalchemy.dialects.postgresql import UUID, JSONB
from sqlalchemy.orm import relationship
import uuid
from datetime import datetime
from aimlpy.model.model_base import Base, ModelBase


class UserActivityRecord(Base, ModelBase):
    __tablename__ = "user_activities"

    activity_id = Column(UUID(as_uuid=True), unique=True, default=uuid.uuid4, nullable=False)
    user_id = Column(UUID(as_uuid=True), ForeignKey('users.user_id'), nullable=False)
    activity_type = Column(String(50), nullable=False)  # e.g., 'view', 'click', 'purchase'
    item_id = Column(String(100), nullable=True)  # ID of the item interacted with
    details = Column(JSONB, nullable=True)  # Additional activity details
    duration = Column(Integer, nullable=True)  # Duration in seconds (if applicable)

    # Relationship
    user = relationship("UserRecord", backref="activities")

    def __repr__(self):
        return f"<UserActivityRecord(user_id='{self.user_id}', activity_type='{self.activity_type}', item_id='{self.item_id}')>"