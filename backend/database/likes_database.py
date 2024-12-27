from backend.model.likes import Like
from sqlalchemy.orm import Session


# 1. いいねを取得する（get）
def get_likes(
    db: Session, user_id: str, question_id: int = None, answer_id: int = None
):
    # ユーザーがしたいいねを取得（質問または回答に関連する）
    query = db.query(Like).filter(Like.user_id == user_id)

    if question_id:
        query = query.filter(Like.question_id == question_id)
    if answer_id:
        query = query.filter(Like.answer_id == answer_id)

    return query.all()


# 2. いいねを作成する（post）
def create_like(
    db: Session, user_id: str, question_id: int = None, answer_id: int = None
):
    # いいねを新規作成
    like = Like(user_id=user_id, question_id=question_id, answer_id=answer_id)
    db.add(like)
    db.commit()
    db.refresh(like)
    return like


# 3. いいねを削除する（delete）
def delete_like(
    db: Session, user_id: str, question_id: int = None, answer_id: int = None
):
    # 指定されたいいねを削除
    like = db.query(Like).filter(Like.user_id == user_id)

    if question_id:
        like = like.filter(Like.question_id == question_id)
    if answer_id:
        like = like.filter(Like.answer_id == answer_id)

    like = like.first()

    if like:
        db.delete(like)
        db.commit()

    return like
