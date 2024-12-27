from backend.model.notifications import Notification
from sqlalchemy.orm import Session


# 1. 通知を取得する（get）
def get_notifications(db: Session, user_id: str, limit: int = 10, offset: int = 0):
    # ユーザーIDに基づいて通知を取得（新しい順）
    return (
        db.query(Notification)
        .filter(Notification.user_id == user_id)
        .order_by(Notification.created_at.desc())
        .limit(limit)
        .offset(offset)
        .all()
    )


# 2. 通知を作成する（post）
def create_notification(
    db: Session,
    user_id: str,
    message: str,
    question_id: int = None,
    answer_id: int = None,
):
    # 新しい通知を作成
    notification = Notification(
        user_id=user_id, message=message, question_id=question_id, answer_id=answer_id
    )
    db.add(notification)
    db.commit()
    db.refresh(notification)
    return notification


# 3. 通知を削除する（delete）
def delete_notification(db: Session, user_id: str, notification_id: int):
    # 指定されたユーザーIDと通知IDに基づいて通知を削除
    notification = (
        db.query(Notification)
        .filter(Notification.user_id == user_id, Notification.id == notification_id)
        .first()
    )
    if notification:
        db.delete(notification)
        db.commit()
    return notification


# 4. 通知を更新する（既読にするなど）
def update_notification(db: Session, user_id: str, notification_id: int, is_read: bool):
    # 指定されたユーザーIDと通知IDに基づいて通知を更新（既読フラグを変更）
    notification = (
        db.query(Notification)
        .filter(Notification.user_id == user_id, Notification.id == notification_id)
        .first()
    )
    if notification:
        notification.is_read = is_read
        db.commit()
        db.refresh(notification)
    return notification
