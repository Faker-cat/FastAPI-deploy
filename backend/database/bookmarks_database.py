from backend.model.bookmarks import Bookmark
from sqlalchemy.orm import Session


# 1. ブックマークの総数を取得する（get）
def read_bookmarks_count(db: Session, question_id: int) -> int:
    # Question.IDに基づいて質問を取得
    query = db.query(Bookmark).filter(Bookmark.question_id == question_id)

    # 結果をカウントして返す
    return query.count()


# 2.自分がブックマークした質問を取得する（get）
def read_my_bookmarks(db: Session, user_id: str):
    bookmarks = db.query(Bookmark).filter(Bookmark.user_id == user_id).all()
    return bookmarks


# 3. ブックマークを作成する（post）
def create_bookmark(db: Session, user_id: str, question_id: int):
    # 同じ質問または回答に対する重複ブックマークを防ぐ
    existing_bookmark = (
        db.query(Bookmark)
        .filter(Bookmark.user_id == user_id, Bookmark.question_id == question_id)
        .first()
    )
    # すでにブックマークが存在する場合、それを返す
    if existing_bookmark:
        return existing_bookmark

    new_bookmark = Bookmark(user_id=user_id, question_id=question_id)
    db.add(new_bookmark)
    db.commit()
    db.refresh(new_bookmark)

    return new_bookmark


# 4. ブックマークを削除する（delete）
def delete_bookmark(db: Session, user_id: str, question_id: int):
    bookmark = (
        db.query(Bookmark)
        .filter(Bookmark.user_id == user_id, Bookmark.question_id == question_id)
        .first()
    )

    if bookmark:
        db.delete(bookmark)
        db.commit()
