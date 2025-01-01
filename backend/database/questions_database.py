from backend.model.questions import Question
from sqlalchemy.orm import Session


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
def update_question(db: Session, user_id: str, question_id: str, new_data: dict):
    # 指定されたユーザーIDと質問IDに基づいて質問を更新
    question = (
        db.query(Question)
        .filter(Question.user_id == user_id, Question.id == question_id)
        .first()
    )
    if question:
        for key, value in new_data.items():
            setattr(question, key, value)  # new_dataのキーと値で属性を更新
        db.commit()
        db.refresh(question)  # 更新された質問を返す
    return question


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
