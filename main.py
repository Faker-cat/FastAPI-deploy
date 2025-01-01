from backend.database.questions_database import (
    create_question,
    delete_question,
    read_my_questions,
    read_questions,
    read_questions_details,
    update_question,
)
from backend.database.users_database import (
    create_user,
    delete_user,
    read_my_user,
    read_users,
    update_user,
)
from backend.middleware.database import get_db
from backend.model.questions import QuestionSchema
from backend.model.users import UserSchema
from fastapi import Depends, FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from sqlalchemy.orm import Session

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


class QuestionCreate(BaseModel):
    title: str
    user_id: str
    is_anonymous: bool
    content: str


class QuestionUpdate(BaseModel):
    title: str
    is_anonymous: bool
    content: str


class UserCreate(BaseModel):
    id: str
    display_name: str
    bio: str


class UserUpdate(BaseModel):
    display_name: str
    bio: str


# 質問
# 1.質問一覧を取得する
@app.get(
    "/questions",
    response_model=list[QuestionSchema],
)
def get_questions(db: Session = Depends(get_db)):
    questions = read_questions(db)
    return [
        QuestionSchema(
            id=q.id,
            title=q.title,
            user_id=str(q.user_id),
            is_anonymous=q.is_anonymous,
            content=q.content,
            created_at=q.created_at,
        )
        for q in questions
    ]


# 2.質問の詳細を取得する
@app.get(
    "/questions/{question_id}",
)
def get_questions_details(question_id: int, db: Session = Depends(get_db)):
    question = read_questions_details(db, question_id)
    # もし対象の質問が存在しない場合、エラーを返す
    if not question:
        raise HTTPException(status_code=404, detail="Question not found")

    # user_id を文字列に変換
    return QuestionSchema(
        id=question.id,
        title=question.title,
        user_id=str(question.user_id),
        is_anonymous=question.is_anonymous,
        content=question.content,
        created_at=question.created_at,
    )
    # return QuestionSchema.model_validate(question)


# 3.自分の質問を取得する
@app.get(
    "/users/{user_id}/questions",
)
def get_my_questions(user_id: str, db: Session = Depends(get_db)):
    questions = read_my_questions(db, user_id)

    # もし対象の質問が存在しない場合、エラーを返す
    if not questions:
        raise HTTPException(status_code=404, detail="Question not found")

    # user_id を文字列に変換
    return [
        QuestionSchema(
            id=q.id,
            title=q.title,
            user_id=str(q.user_id),  # UUIDを文字列に変換
            is_anonymous=q.is_anonymous,
            content=q.content,
            created_at=q.created_at,
        )
        for q in questions
    ]
    # return [QuestionSchema.model_validate(q) for q in questions]


# 4.新しい質問を作成する
@app.post(
    "/questions",
)
def post_question(question: QuestionCreate, db: Session = Depends(get_db)):
    post_question = create_question(
        db, question.title, question.user_id, question.is_anonymous, question.content
    )
    return post_question


# 5.質問を削除する
@app.delete("/questions/{user_id}/{question_id}")
def delete_question_endpoint(
    user_id: str, question_id: int, db: Session = Depends(get_db)
):
    delete_question(db, user_id, question_id)
    # if not question:
    #     raise HTTPException(status_code=404, detail="Question not found")
    # # return QuestionSchema.model_validate(question)


# 6.質問を編集（更新）する
@app.put("/questions/{user_id}/{question_id}")
def update_question_endpoint(
    user_id: str,
    question_id: int,
    question: QuestionUpdate,
    db: Session = Depends(get_db),
):
    put_question = update_question(db, user_id, question_id, question)
    if not put_question:
        raise HTTPException(status_code=404, detail="Question not found")
    # return QuestionSchema(
    #     id=put_question.id,
    #     title=put_question.title,
    #     user_id=str(put_question.user_id),
    #     is_anonymous=put_question.is_anonymous,
    #     content=put_question.content,
    #     created_at=put_question.created_at,
    # )
    return put_question


# ユーザ
# 1.ユーザ一覧を取得する(編集用)
@app.get(
    "/users",
    response_model=list[UserSchema],
)
def get_users(db: Session = Depends(get_db)):
    users = read_users(db)
    return [
        UserSchema(id=str(q.id), display_name=q.display_name, bio=q.bio) for q in users
    ]


# 2.自分のユーザ情報を取得する
@app.get(
    "/users/{id}/users",
)
def get_my_user(user_id: str, db: Session = Depends(get_db)):
    user = read_my_user(db, user_id)

    # もし対象の質問が存在しない場合、エラーを返す
    if not user:
        raise HTTPException(status_code=404, detail="User not found")

    return UserSchema(id=str(user.id), display_name=user.display_name, bio=user.bio)


# 2.ユーザを作成する
@app.post(
    "/users/",
)
def post_user(user: UserCreate, db: Session = Depends(get_db)):
    post_user = create_user(db, user.id, user.display_name, user.bio)
    return post_user


# 4.ユーザを削除する
@app.delete("/users/{id}/")
def delete_user_endpoint(id: str, db: Session = Depends(get_db)):
    delete_user(db, id)


# 5.ユーザを編集（更新）する
@app.put("/users/{id}/")
def update_user_endpoint(
    id: str,
    user: UserUpdate,
    db: Session = Depends(get_db),
):
    put_user = update_user(db, id, user)
    if not put_user:
        raise HTTPException(status_code=404, detail="User not found")
    return put_user
