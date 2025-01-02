from backend.model.likes import Like
from sqlalchemy.orm import Session

# 0. いいねを取得する（get）
# def get_likes(
#     db: Session, user_id: str, question_id: int = None, answer_id: int = None
# ):
#     # ユーザーがしたいいねを取得（質問または回答に関連する）
#     query = db.query(Like).filter(Like.user_id == user_id)

#     if question_id:
#         query = query.filter(Like.question_id == question_id)
#     if answer_id:
#         query = query.filter(Like.answer_id == answer_id)

#     return query.all()


# 1. いいねの総数を取得する（get）
def read_likes_count(
    db: Session, question_id: int = None, answer_id: int = None
) -> int:
    # ベースとなるクエリを作成
    query = db.query(Like)

    # 質問IDが指定されていればフィルタリング
    if question_id:
        query = query.filter(Like.question_id == question_id)

    # 回答IDが指定されていればフィルタリング
    if answer_id:
        query = query.filter(Like.answer_id == answer_id)

    # 結果をカウントして返す
    return query.count()


# 2.自分がいいねした質問、回答を取得する（get）
def read_my_likes(db: Session, user_id: str):
    likes = db.query(Like).filter(Like.user_id == user_id).all()
    return likes


# 3. いいねを作成する（post）
def create_like(
    db: Session, user_id: str, question_id: int = None, answer_id: int = None
):
    # 同じ質問または回答に対する重複いいねを防ぐ
    existing_like = (
        db.query(Like)
        .filter(
            Like.user_id == user_id,
            (Like.question_id == question_id) if question_id else True,
            (Like.answer_id == answer_id) if answer_id else True,
        )
        .first()
    )
    # すでにいいねが存在する場合、それを返す
    if existing_like:
        return existing_like

    new_like = Like(user_id=user_id, question_id=question_id, answer_id=answer_id)
    db.add(new_like)
    db.commit()
    db.refresh(new_like)

    return new_like


# 4. いいねを削除する（delete）
def delete_like(
    db: Session, user_id: str, question_id: int = None, answer_id: int = None
):
    like = (
        db.query(Like)
        .filter(
            Like.user_id == user_id,
            (Like.question_id == question_id) if question_id else True,
            (Like.answer_id == answer_id) if answer_id else True,
        )
        .first()
    )

    if like:
        db.delete(like)
        db.commit()
