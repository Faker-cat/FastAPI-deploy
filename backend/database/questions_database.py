from backend.model.questions import Question
from pydantic import BaseModel
from sqlalchemy.orm import Session


class QuestionUpdate(BaseModel):
    title: str
    is_anonymous: bool
    content: str


# 1. 質問を取得する（get）
def read_questions(db: Session):
    # 質問を新しい順に取得
    questions = db.query(Question).order_by(Question.created_at.desc()).all()
    return questions


# 2. 新しい質問を作成する（post）
def create_question(db: Session, question: Question):
    # 新しい質問をデータベースに追加
    db.add(question)
    db.commit()
    db.refresh(question)  # 作成された質問を返す
    return question


# 3. 質問を削除する（delete）
def delete_question(db: Session, user_id: str, question_id: int):
    # 指定されたユーザーIDと質問IDに基づいて質問を削除
    question = (
        db.query(Question)
        .filter(Question.user_id == user_id, Question.id == question_id)
        .first()
    )
    if question:
        db.delete(question)
        db.commit()
    return question


# 4. 質問を編集する（更新）
def update_question(
    db: Session, user_id: str, question_id: int, question: QuestionUpdate
):
    # 指定されたユーザーIDと質問IDに基づいて質問を更新
    put_question = (
        db.query(Question)
        .filter(Question.user_id == user_id, Question.id == question_id)
        .first()
    )
    if not put_question:
        None

    put_question.title = question.title
    put_question.is_anonymous = question.is_anonymous
    put_question.content = question.content
    db.commit()
    db.refresh(put_question)  # 更新された質問を返す
    return put_question


# 5. 質問の詳細を取得する（get）
def read_questions_details(db: Session, question_id: int):
    # Question.IDに基づいて質問を取得
    question = db.query(Question).filter(Question.id == question_id).first()
    return question


# 6. 自分の質問を取得する（get）
def read_my_questions(db: Session, user_id: str):
    # ユーザーIDに基づいて質問を取得（質問を新しい順に取得）
    questions = (
        db.query(Question)
        .filter(Question.user_id == user_id)
        .order_by(Question.created_at.desc())
        .all()
    )
    return questions
