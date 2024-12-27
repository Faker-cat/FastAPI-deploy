from backend.model.tags import Question, Tag
from sqlalchemy.orm import Session


# 1. タグを取得する（get）
def read_tag(db: Session, tag_id: int):
    # タグIDに基づいてタグ情報を取得
    tag = db.query(Tag).filter(Tag.id == tag_id).first()
    return tag


# 2. 新しいタグを作成する（post）
def create_tag(db: Session, tag_name: str):
    # 新しいタグを作成し、データベースに追加
    tag = Tag(name=tag_name)  # タグ名を使ってTagインスタンスを作成
    db.add(tag)
    db.commit()
    db.refresh(tag)  # 作成されたタグを返す
    return tag


# 3. タグを削除する（delete）
def delete_tag(db: Session, tag_id: int):
    # 指定されたタグIDに基づいてタグを削除
    tag = db.query(Tag).filter(Tag.id == tag_id).first()
    if tag:
        db.delete(tag)
        db.commit()
    return tag


# 4. 質問にタグを追加する（add_tag_to_question）
def add_tag_to_question(db: Session, question_id: int, tag_ids: list):
    # 質問にタグを追加する（多対多のリレーションを使う）
    question = db.query(Question).filter(Question.id == question_id).first()
    if question:
        # タグIDリストからタグを取得して質問に追加
        tags = db.query(Tag).filter(Tag.id.in_(tag_ids)).all()
        question.tags.extend(tags)  # 質問にタグを追加
        db.commit()
        db.refresh(question)
    return question
