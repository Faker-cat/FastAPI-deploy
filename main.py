from backend.database.answers_database import (
    create_answer,
    delete_answer,
    read_answers,
    read_my_answers,
    read_question_answers,
    update_answer,
)
from backend.database.bookmarks_database import (
    create_bookmark,
    delete_bookmark,
    read_bookmarks_count,
    read_my_bookmarks,
)
from backend.database.likes_database import (
    create_like,
    delete_like,
    read_likes_count,
    read_my_likes,
)
from backend.database.questions_database import (
    create_question,
    delete_question,
    read_my_questions,
    read_questions,
    read_questions_details,
    update_question,
)
from backend.database.tags_database import (
    add_tag_to_question,
    create_tag,
    delete_tag,
    read_tag,
)
from backend.database.users_database import (
    create_user,
    delete_user,
    read_my_user,
    read_users,
    update_user,
)
from backend.middleware.database import get_db
from backend.model.answers import AnswerSchema
from backend.model.questions import QuestionSchema
from backend.model.tags import TagSchema
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
    expose_headers=["*"],
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


class AnswerCreate(BaseModel):
    user_id: str
    is_anonymous: bool
    content: str


class AnswerUpdate(BaseModel):
    is_anonymous: bool
    content: str


class UserCreate(BaseModel):
    id: str
    display_name: str
    bio: str


class UserUpdate(BaseModel):
    display_name: str
    bio: str


class TagCreate(BaseModel):
    name: str


# 質問
# 1.質問一覧を取得する
@app.get(
    "/questions",
    response_model=list[QuestionSchema],
)
def get_questions(db: Session = Depends(get_db)):
    questions = read_questions(db)
    return [QuestionSchema.model_validate(q) for q in questions]


# 2.質問の詳細を取得する
@app.get(
    "/questions/{question_id}",
)
def get_questions_details(question_id: int, db: Session = Depends(get_db)):
    question = read_questions_details(db, question_id)
    # もし対象の質問が存在しない場合、エラーを返す
    if not question:
        raise HTTPException(status_code=404, detail="Question not found")

    for tag in question.tags:
        print(f"Tag ID: {tag.id}, Name: {tag.name}")

    return QuestionSchema.model_validate(question)


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


# 回答
# 1.回答一覧を取得する(仮)
@app.get(
    "/answers",
    response_model=list[AnswerSchema],
)
def get_answers(db: Session = Depends(get_db)):
    answers = read_answers(db)
    return [
        AnswerSchema(
            id=q.id,
            question_id=q.question_id,
            user_id=str(q.user_id),
            is_anonymous=q.is_anonymous,
            content=q.content,
            created_at=q.created_at,
        )
        for q in answers
    ]


# 2.特定の質問に対する回答を取得する
@app.get(
    "/answers/{question_id}",
)
def get_question_answers(question_id: int, db: Session = Depends(get_db)):
    answers = read_question_answers(db, question_id)
    # もし対象の質問が存在しない場合、エラーを返す
    if not answers:
        raise HTTPException(status_code=404, detail="Answers not found")

    # user_id を文字列に変換
    # AnswerSchema(
    #     id=answers.id,
    #     question_id=answers.question_id,
    #     user_id=str(answers.user_id),
    #     is_anonymous=answers.is_anonymous,
    #     content=answers.content,
    #     created_at=answers.created_at,
    # )
    return answers
    # return QuestionSchema.model_validate(question)


# 3.自分の回答を取得する
@app.get(
    "/answers/{user_id}/answers",
)
def get_my_answers(user_id: str, db: Session = Depends(get_db)):
    answers = read_my_answers(db, user_id)

    # もし対象の質問が存在しない場合、エラーを返す
    if not answers:
        raise HTTPException(status_code=404, detail="Answers not found")

    # user_id を文字列に変換
    # return [
    #     AnswerSchema(
    #         id=q.id,
    #         question_id=q.question_id,
    #         user_id=str(q.user_id),  # UUIDを文字列に変換
    #         is_anonymous=q.is_anonymous,
    #         content=q.content,
    #         created_at=q.created_at,
    #     )
    #     for q in answers
    # ]
    return answers
    # return [QuestionSchema.model_validate(q) for q in questions]


# 4.新しい回答を作成する
@app.post(
    "/answers",
)
def post_answer(question_id: int, answer: AnswerCreate, db: Session = Depends(get_db)):
    post_answer = create_answer(
        db, question_id, answer.user_id, answer.is_anonymous, answer.content
    )
    return post_answer


# 5.回答を削除する
@app.delete("/answers/{user_id}/{answer_id}")
def delete_answer_endpoint(user_id: str, answer_id: int, db: Session = Depends(get_db)):
    delete_answer(db, user_id, answer_id)
    # if not question:
    #     raise HTTPException(status_code=404, detail="Question not found")
    # # return QuestionSchema.model_validate(question)


# 6.回答を編集（更新）する
@app.put("/answers/{user_id}/{answer_id}")
def update_answer_endpoint(
    user_id: str,
    answer_id: int,
    answer: AnswerUpdate,
    db: Session = Depends(get_db),
):
    put_answer = update_answer(db, user_id, answer_id, answer)
    if not put_answer:
        raise HTTPException(status_code=404, detail="Answer not found")

    return put_answer


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
def get_my_user(id: str, db: Session = Depends(get_db)):
    user = read_my_user(db, id)

    # もし対象の質問が存在しない場合、エラーを返す
    if not user:
        raise HTTPException(status_code=404, detail="User not found")

    return UserSchema(id=str(user.id), display_name=user.display_name, bio=user.bio)


@app.get(
    "/users/{id}/exists",
)
def exists_user(id: str, db: Session = Depends(get_db)):
    user = read_my_user(db, id)

    # もし対象の質問が存在しない場合、エラーを返す
    if not user:
        return {"exists": False}
    return {"exists": True}


# 2.ユーザを作成する
@app.post(
    "/users",
)
def post_user(user: UserCreate, db: Session = Depends(get_db)):
    post_user = create_user(db, user.id, user.display_name, user.bio)
    return post_user


# 4.ユーザを削除する
@app.delete("/users/{id}")
def delete_user_endpoint(id: str, db: Session = Depends(get_db)):
    delete_user(db, id)


# 5.ユーザを編集（更新）する
@app.put("/users/{id}")
def update_user_endpoint(
    id: str,
    user: UserUpdate,
    db: Session = Depends(get_db),
):
    put_user = update_user(db, id, user)
    if not put_user:
        raise HTTPException(status_code=404, detail="User not found")
    return put_user


# いいね
# 1. いいねの総数を取得する（質問または回答に対して）
@app.get("/likes/count")
def get_likes_count(
    question_id: int = None, answer_id: int = None, db: Session = Depends(get_db)
):
    if not question_id and not answer_id:
        raise HTTPException(
            status_code=400, detail="Question ID or Answer ID must be provided"
        )
    likes_count = read_likes_count(db, question_id, answer_id)
    return {"total_likes": likes_count}


# 2. ユーザーがいいねした質問・回答を取得する
@app.get("/users/{user_id}/likes")
def get_user_likes(user_id: str, db: Session = Depends(get_db)):
    likes = read_my_likes(db, user_id)
    if not likes:
        raise HTTPException(status_code=404, detail="No likes found for this user")
    return [
        {"id": like.id, "question_id": like.question_id, "answer_id": like.answer_id}
        for like in likes
    ]


# 3. いいねを追加する
@app.post("/likes")
def add_like(
    user_id: str,
    question_id: int = None,
    answer_id: int = None,
    db: Session = Depends(get_db),
):
    if not question_id and not answer_id:
        raise HTTPException(
            status_code=400, detail="Question ID or Answer ID must be provided"
        )

    new_like = create_like(db, user_id, question_id, answer_id)
    return {"message": "Like added successfully", "like": new_like}


# 4. いいねを削除する
@app.delete("/likes")
def remove_like(
    user_id: str,
    question_id: int = None,
    answer_id: int = None,
    db: Session = Depends(get_db),
):
    delete_like(db, user_id, question_id, answer_id)


# ブックマーク
# 1. ブックマークの総数を取得する（質問または回答に対して）
@app.get("/bookmarks/count")
def get_bookmarks_count(question_id: int, db: Session = Depends(get_db)):
    if not question_id:
        raise HTTPException(status_code=400, detail="Question ID must be provided")
    bookmarks_count = read_bookmarks_count(db, question_id)
    return {"total_bookmarks": bookmarks_count}


# 2. ユーザーがブックマークした質問を取得する
@app.get("/users/{user_id}/bookmarks")
def get_user_bookmarks(user_id: str, db: Session = Depends(get_db)):
    bookmarks = read_my_bookmarks(db, user_id)
    if not bookmarks:
        raise HTTPException(status_code=404, detail="No bookmarks found for this user")
    return [
        {"id": bookmark.id, "question_id": bookmark.question_id}
        for bookmark in bookmarks
    ]


# 3. ブックマークを追加する
@app.post("/bookmarks")
def add_bookmark(
    user_id: str,
    question_id: int = None,
    db: Session = Depends(get_db),
):
    if not question_id:
        raise HTTPException(status_code=400, detail="Question ID must be provided")

    new_bookmark = create_bookmark(db, user_id, question_id)
    return {"message": "Bookmark added successfully", "bookmark": new_bookmark}


# 4. ブックマークを削除する
@app.delete("/bookmarks")
def remove_bookmark(
    user_id: str,
    question_id: int = None,
    db: Session = Depends(get_db),
):
    delete_bookmark(db, user_id, question_id)


# --- タグ管理エンドポイント ---


# タグ
# 1. タグを取得する
@app.get("/tags/{tag_id}", response_model=TagSchema)
def get_tag(tag_id: int, db: Session = Depends(get_db)):
    tag = read_tag(db, tag_id)
    if not tag:
        raise HTTPException(status_code=404, detail="Tag not found")
    return TagSchema(id=tag.id, name=tag.name)


# 2. 新しいタグを作成する
@app.post("/tags", response_model=TagSchema)
def create_new_tag(tag: TagCreate, db: Session = Depends(get_db)):
    new_tag = create_tag(db, tag.name)
    return TagSchema(id=new_tag.id, name=new_tag.name)


# 3. タグを削除する
@app.delete("/tags/{tag_id}")
def delete_existing_tag(tag_id: int, db: Session = Depends(get_db)):
    tag = delete_tag(db, tag_id)
    if not tag:
        raise HTTPException(status_code=404, detail="Tag not found")
    return {"message": "Tag deleted successfully"}


# --- 質問にタグを追加するエンドポイント ---
@app.post("/questions/{question_id}/tags")
def add_tags_to_question(
    question_id: int, tag_ids: list[int], db: Session = Depends(get_db)
):
    question = add_tag_to_question(db, question_id, tag_ids)
    if not question:
        raise HTTPException(status_code=404, detail="Question not found")
    return {"message": "Tags added to the question successfully", "tags": tag_ids}
