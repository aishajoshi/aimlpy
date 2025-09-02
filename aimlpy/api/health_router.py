"""
-- Created by: Ashok Kumar Pant
-- Email: asokpant@gmail.com
-- Created on: 04/05/2025
"""
from fastapi import APIRouter
from aimlpy.entity.common import BaseResponse

router = APIRouter(prefix="/health", tags=["health"])


@router.get("", response_model=BaseResponse)
async def health_check():
    """
    Health check endpoint
    """
    return BaseResponse(message="Service is healthy")


@router.get("/ready", response_model=BaseResponse)
async def readiness_check():
    """
    Readiness check endpoint
    """
    return BaseResponse(message="Service is ready")