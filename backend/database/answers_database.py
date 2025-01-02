from backend.model.answers import Answer
from pydantic import BaseModel
from sqlalchemy.orm import Session


class AnswerUpdate(BaseModel):
    is_anonymous: bool
    content: str


# 1. 回答一覧を取得する（get）
def read_answers(db: Session):
    # 回答を新しい順に取得
    answers = db.query(Answer).order_by(Answer.created_at.desc()).all()
    return answers


# 2. 特定の質問に対する回答を取得する（get）
def read_question_answers(db: Session, question_id: int):
    # Question.IDに基づいて回答を取得
    answers = db.query(Answer).filter(Answer.question_id == question_id).first()
    return answers


# 3. 自分の回答を取得する（get）
def read_my_answers(db: Session, user_id: str):
    # ユーザーIDに基づいて回答を取得（回答を新しい順に取得）
    answers = (
        db.query(Answer)
        .filter(Answer.user_id == user_id)
        .order_by(Answer.created_at.desc())
        .all()
    )
    return answers


# 4. 新しい回答を作成する（post）
def create_answer(
    db: Session, question_id: int, user_id: str, is_anonymous: bool, content: str
):
    answer = Answer(
        question_id=question_id,
        user_id=user_id,
        is_anonymous=is_anonymous,
        content=content,
    )
    # 新しい質問をデータベースに追加
    db.add(answer)
    db.commit()
    db.refresh(answer)  # 作成された質問を返す
    return answer


# 5. 回答を削除する（delete）
def delete_answer(db: Session, user_id: str, answer_id: int):
    # 指定された回答IDとユーザーIDに基づいて回答を削除
    answer = (
        db.query(Answer)
        .filter(Answer.id == answer_id, Answer.user_id == user_id)
        .first()
    )
    if answer:
        db.delete(answer)
        db.commit()


# 6. 回答を編集する（更新）
def update_answer(db: Session, user_id: str, answer_id: int, answer: AnswerUpdate):
    # 指定された回答IDとユーザーIDに基づいて回答を更新
    put_answer = (
        db.query(Answer)
        .filter(Answer.id == answer_id, Answer.user_id == user_id)
        .first()
    )
    if not put_answer:
        None

    put_answer.is_anonymous = answer.is_anonymous
    put_answer.content = answer.content
    db.commit()
    db.refresh(put_answer)
    return put_answer
