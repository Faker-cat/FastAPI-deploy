from backend.model.bookmarks import Bookmark
from sqlalchemy.orm import Session


# 1. ブックマークを取得する（get）
def get_bookmarks(db: Session, user_id: str, question_id: int):
    # ユーザーがしたブックマークを取得
    return (
        db.query(Bookmark)
        .filter(Bookmark.user_id == user_id, Bookmark.question_id == question_id)
        .all()
    )


# 2. ブックマークを作成する（post）
def create_bookmark(db: Session, user_id: str, question_id: int):
    # 新規にブックマークを作成
    bookmark = Bookmark(user_id=user_id, question_id=question_id)
    db.add(bookmark)
    db.commit()
    db.refresh(bookmark)
    return bookmark


# 3. ブックマークを削除する（delete）
def delete_bookmark(db: Session, user_id: str, question_id: int):
    # 指定されたユーザーIDと質問IDに基づいてブックマークを削除
    bookmark = (
        db.query(Bookmark)
        .filter(Bookmark.user_id == user_id, Bookmark.question_id == question_id)
        .first()
    )

    if bookmark:
        db.delete(bookmark)
        db.commit()

    return bookmark
