from typing import Any, Dict, List

from backend.database.questions_database import (
    create_question,
    delete_question,
    read_questions,
    update_question,
)
from backend.middleware.database import get_db
from backend.model.questions import Question
from fastapi import Depends, FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from sqlalchemy.orm import Session

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.get("/")
async def root():
    return {"message": "Hello World From Fast API!"}

    # ルートエンドポイント（ホーム）


@app.get("/")
async def root():
    return {"message": "Hello World From Fast API!"}


# 質問一覧を取得するエンドポイント
@app.get("/questions/{user_id}", response_model=List[Question])
def get_questions(user_id: str, db: Session = Depends(get_db)):
    return read_questions(db, user_id)


# 新しい質問を作成するエンドポイント
@app.post("/questions/", response_model=Question)
def post_question(question: Question, db: Session = Depends(get_db)):
    return create_question(db, question)


# 質問を削除するエンドポイント
@app.delete("/questions/{user_id}/{question_id}", response_model=Question)
def delete_question_endpoint(
    user_id: str, question_id: str, db: Session = Depends(get_db)
):
    question = delete_question(db, user_id, question_id)
    if not question:
        raise HTTPException(status_code=404, detail="Question not found")
    return question


# 質問を編集（更新）するエンドポイント
@app.put("/questions/{user_id}/{question_id}", response_model=Question)
def update_question_endpoint(
    user_id: str,
    question_id: str,
    new_data: Dict[str, Any],
    db: Session = Depends(get_db),
):
    question = update_question(db, user_id, question_id, new_data)
    if not question:
        raise HTTPException(status_code=404, detail="Question not found")
    return question
