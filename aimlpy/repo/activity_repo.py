
from typing import List, Dict, Optional
from datetime import datetime, timedelta
from sqlalchemy import func, desc
from aimlpy.model.user_activity_record import UserActivityRecord
from aimlpy.repo.datasource import DataSource
from aimlpy.util import loggerutil
import uuid


class ActivityRepo:
    def __init__(self, db: DataSource):
        self.db = db
        self.logger = loggerutil.get_logger(__name__)

    def track_activity(self, user_id: str, activity_type: str, item_id: Optional[str] = None,
                       details: Optional[Dict] = None, duration: Optional[int] = None) -> UserActivityRecord:
        """
        Track a user activity
        """
        with self.db.session_scope() as session:
            try:
                activity = UserActivityRecord(
                    user_id=uuid.UUID(user_id),
                    activity_type=activity_type,
                    item_id=item_id,
                    details=details,
                    duration=duration
                )
                session.add(activity)
                session.commit()
                session.refresh(activity)
                return activity
            except Exception as e:
                session.rollback()
                self.logger.error(f"Error tracking activity: {e}")
                raise

    def get_user_activities(self, user_id: str, limit: int = 100) -> List[UserActivityRecord]:
        """
        Get recent activities for a user
        """
        with self.db.get_session() as session:
            try:
                activities = session.query(UserActivityRecord) \
                    .filter(UserActivityRecord.user_id == uuid.UUID(user_id)) \
                    .order_by(desc(UserActivityRecord.created_at)) \
                    .limit(limit) \
                    .all()
                return activities
            except Exception as e:
                self.logger.error(f"Error getting activities for user {user_id}: {e}")
                raise

    def get_recent_items(self, user_id: str, activity_type: str, limit: int = 10) -> List[str]:
        """
        Get recent items a user interacted with for a specific activity type
        """
        with self.db.get_session() as session:
            try:
                items = session.query(UserActivityRecord.item_id) \
                    .filter(
                    UserActivityRecord.user_id == uuid.UUID(user_id),
                    UserActivityRecord.activity_type == activity_type,
                    UserActivityRecord.item_id.isnot(None)
                ) \
                    .order_by(desc(UserActivityRecord.created_at)) \
                    .limit(limit) \
                    .all()
                return [item[0] for item in items if item[0]]
            except Exception as e:
                self.logger.error(f"Error getting recent items for user {user_id}: {e}")
                raise

    def get_activity_stats(self, user_id: str) -> Dict:
        """
        Get activity statistics for a user
        """
        with self.db.get_session() as session:
            try:
                # Total activities
                total = session.query(func.count(UserActivityRecord.id)) \
                    .filter(UserActivityRecord.user_id == uuid.UUID(user_id)) \
                    .scalar()

                # Activities by type
                by_type = session.query(
                    UserActivityRecord.activity_type,
                    func.count(UserActivityRecord.id)
                ) \
                    .filter(UserActivityRecord.user_id == uuid.UUID(user_id)) \
                    .group_by(UserActivityRecord.activity_type) \
                    .all()

                # Last activity
                last_activity = session.query(UserActivityRecord.created_at) \
                    .filter(UserActivityRecord.user_id == uuid.UUID(user_id)) \
                    .order_by(desc(UserActivityRecord.created_at)) \
                    .first()

                return {
                    "total_activities": total or 0,
                    "activity_types": dict(by_type) if by_type else {},
                    "last_activity": last_activity[0] if last_activity else None
                }
            except Exception as e:
                self.logger.error(f"Error getting activity stats for user {user_id}: {e}")
                raise