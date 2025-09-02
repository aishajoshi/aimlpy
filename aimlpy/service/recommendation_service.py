"""
-- Created by: Ashok Kumar Pant
-- Email: asokpant@gmail.com
-- Created on: 04/05/2025
"""
from typing import List, Dict
from datetime import datetime
import logging
import uuid
from sqlalchemy.orm import Session
from aimlpy.entity.recommendation_reqres import GetRecommendationResponse
from aimlpy.entity.recommendation import Recommendation
from aimlpy.entity.common import ErrorCode
from aimlpy.model.recommendation_record import RecommendationRecord
from aimlpy.model.user_record import UserRecord
from aimlpy.repo.activity_repo import ActivityRepo

logger = logging.getLogger(__name__)


class RecommendationService:
    def __init__(self, db: Session, activity_repo: ActivityRepo):
        self.db = db
        self.activity_repo = activity_repo

    async def get_recommendations(self, user_id: str, top_k: int = 10) -> GetRecommendationResponse:
        """
        Get personalized recommendations for a user based on their activity
        """
        try:
            if not user_id:
                return self._create_error_response(user_id, "User ID is required", ErrorCode.BAD_REQUEST)

            # Check if user exists
            user = self.db.query(UserRecord).filter(UserRecord.user_id == uuid.UUID(user_id)).first()
            if not user:
                return self._create_error_response(user_id, f"User with ID {user_id} not found", ErrorCode.NOT_FOUND)

            # Generate recommendations based on user activity
            raw_recommendations = await self._generate_personalized_recommendations(user_id)

            # Save recommendations to database
            self._save_recommendations(user_id, raw_recommendations)

            # Convert to Recommendation objects
            recommendations = [
                Recommendation(
                    item_id=rec["item_id"],
                    score=rec["score"],
                    reason=rec.get("reason", "Based on your activity and preferences"),
                    metadata=rec.get("metadata", {})
                )
                for rec in raw_recommendations[:top_k]
            ]

            return GetRecommendationResponse(
                user_id=user_id,
                recommendations=recommendations,
                total_count=len(recommendations),
                generated_at=datetime.now(),
                message="Personalized recommendations generated based on your activity"
            )

        except Exception as e:
            logger.error(f"Error getting recommendations for user {user_id}: {str(e)}")
            return self._create_error_response(user_id, f"Internal server error: {str(e)}",
                                               ErrorCode.INTERNAL_SERVER_ERROR)

    async def _generate_personalized_recommendations(self, user_id: str) -> List[Dict]:
        """
        Generate recommendations based on user activity history
        """
        # Get user's recent activities
        recent_views = self.activity_repo.get_recent_items(user_id, "view", 10)
        recent_clicks = self.activity_repo.get_recent_items(user_id, "click", 10)
        recent_purchases = self.activity_repo.get_recent_items(user_id, "purchase", 5)

        # Combine all recent interactions
        all_interactions = recent_views + recent_clicks + recent_purchases

        if all_interactions:
            # If user has activity history, generate personalized recommendations
            return self._generate_based_on_activity(all_interactions, user_id)
        else:
            # Fallback to general recommendations for new users
            return await self._generate_general_recommendations()

    def _generate_based_on_activity(self, interactions: List[str], user_id: str) -> List[Dict]:
        """
        Generate recommendations based on user's interaction history
        """
        # This is a simplified example - replace with your actual recommendation algorithm
        recommendations = []

        # Example: Recommend similar items to what the user interacted with
        for i, item_id in enumerate(interactions[:5]):  # Top 5 interacted items
            recommendations.append({
                "item_id": f"similar_to_{item_id}",
                "score": 0.9 - (i * 0.1),  # Decreasing score for less recent items
                "reason": f"Similar to items you recently interacted with",
                "metadata": {"based_on": item_id, "type": "similar_item"}
            })

        # Example: Recommend popular items in same category
        recommendations.extend([
            {
                "item_id": "popular_1",
                "score": 0.85,
                "reason": "Popular among users with similar activity",
                "metadata": {"type": "popular"}
            },
            {
                "item_id": "popular_2",
                "score": 0.82,
                "reason": "Trending in categories you're interested in",
                "metadata": {"type": "trending"}
            }
        ])

        return recommendations

    async def _generate_general_recommendations(self) -> List[Dict]:
        """
        Generate general recommendations for new users
        """
        return [
            {"item_id": "1", "score": 0.95, "reason": "Highly popular among all users",
             "metadata": {"category": "electronics"}},
            {"item_id": "2", "score": 0.88, "reason": "New arrival that's getting great reviews",
             "metadata": {"category": "books"}},
            {"item_id": "3", "score": 0.82, "reason": "Best seller in your region",
             "metadata": {"category": "clothing"}},
        ]

    def _save_recommendations(self, user_id: str, recommendations: List[Dict]):
        """Save recommendations to database"""
        for rec in recommendations:
            recommendation_record = RecommendationRecord(
                user_id=uuid.UUID(user_id),
                item_id=rec["item_id"],
                score=rec["score"],
                reason=rec.get("reason"),
                metadata=rec.get("metadata", {})
            )
            self.db.add(recommendation_record)

        self.db.commit()

    def _create_error_response(self, user_id: str, message: str, error_code: ErrorCode) -> GetRecommendationResponse:
        """Helper method to create error responses"""
        return GetRecommendationResponse(
            error=True,
            error_code=error_code,
            message=message,
            user_id=user_id,
            recommendations=[],
            total_count=0,
            generated_at=datetime.now()
        )