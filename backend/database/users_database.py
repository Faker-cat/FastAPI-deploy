from backend.model.users import User
from pydantic import BaseModel
from sqlalchemy.orm import Session


class UserUpdate(BaseModel):
    display_name: str
    bio: str


# 1. ユーザ情報一覧を取得する（get）
def read_users(db: Session):
    # ユーザを新しい順に取得
    users = db.query(User).order_by(User.created_at.desc()).all()
    return users


# 2. ユーザー情報を取得する（get）
def read_my_user(db: Session, user_id: str):
    # ユーザーIDに基づいてユーザー情報を取得
    user = db.query(User).filter(User.id == user_id).first()
    return user


# 3. 新しいユーザーを作成する（post）
def create_user(db: Session, id, display_name, bio):
    # 新しいユーザーを作成し、データベースに追加
    user = User(
        id=id, display_name=display_name, bio=bio
    )  # user_dataの情報を使ってUserインスタンスを作成
    db.add(user)
    db.commit()
    db.refresh(user)  # 作成されたユーザーを返す
    return user


# 4. 質問を削除する（delete）
def delete_user(db: Session, id: str):
    # 指定されたユーザーIDと質問IDに基づいて質問を削除
    user = db.query(User).filter(User.id == id).first()
    if user:
        db.delete(user)
        db.commit()
    return user


# 5. ユーザー情報を更新する（update）
def update_user(db: Session, id: str, user: UserUpdate):
    # 指定されたユーザーIDに基づいてユーザー情報を更新
    put_user = db.query(User).filter(User.id == id).first()
    if not put_user:
        None

    put_user.display_name = user.display_name
    put_user.bio = user.bio

    db.commit()
    db.refresh(put_user)  # 更新されたユーザ情報を返す
    return put_user
