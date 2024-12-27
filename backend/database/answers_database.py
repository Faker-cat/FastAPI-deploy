from backend.model.answers import Answer
from sqlalchemy.orm import Session


# 1. 回答を取得する（get）
def read_answer(db: Session, answer_id: int):
    # 回答IDに基づいて回答情報を取得
    answer = db.query(Answer).filter(Answer.id == answer_id).first()
    return answer


# 2. 新しい回答を作成する（post）
def create_answer(db: Session, answer_data: dict):
    # 新しい回答を作成し、データベースに追加
    answer = Answer(**answer_data)  # answer_dataの情報を使ってAnswerインスタンスを作成
    db.add(answer)
    db.commit()
    db.refresh(answer)  # 作成された回答を返す
    return answer


# 3. 回答を削除する（delete）
def delete_answer(db: Session, answer_id: int, user_id: str):
    # 指定された回答IDとユーザーIDに基づいて回答を削除
    answer = (
        db.query(Answer)
        .filter(Answer.id == answer_id, Answer.user_id == user_id)
        .first()
    )
    if answer:
        db.delete(answer)
        db.commit()
    return answer


# 4. 回答を編集する（更新）
def update_answer(db: Session, answer_id: int, user_id: str, new_data: dict):
    # 指定された回答IDとユーザーIDに基づいて回答を更新
    answer = (
        db.query(Answer)
        .filter(Answer.id == answer_id, Answer.user_id == user_id)
        .first()
    )
    if answer:
        for key, value in new_data.items():
            setattr(answer, key, value)  # new_dataのキーと値で属性を更新
        db.commit()
        db.refresh(answer)  # 更新された回答を返す
    return answer
