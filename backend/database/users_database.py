from backend.model.users import User
from sqlalchemy.orm import Session


# 1. ユーザー情報を取得する（get）
def read_user(db: Session, user_id: str):
    # ユーザーIDに基づいてユーザー情報を取得
    user = db.query(User).filter(User.id == user_id).first()
    return user


# 2. 新しいユーザーを作成する（post）
def create_user(db: Session, user_data: dict):
    # 新しいユーザーを作成し、データベースに追加
    user = User(**user_data)  # user_dataの情報を使ってUserインスタンスを作成
    db.add(user)
    db.commit()
    db.refresh(user)  # 作成されたユーザーを返す
    return user


# 3. ユーザー情報を更新する（update）
def update_user(db: Session, user_id: str, new_data: dict):
    # 指定されたユーザーIDに基づいてユーザー情報を更新
    user = db.query(User).filter(User.id == user_id).first()
    if user:
        for key, value in new_data.items():
            setattr(user, key, value)  # new_dataのキーと値で属性を更新
        db.commit()
        db.refresh(user)  # 更新されたユーザーを返す
    return user


# 4. ユーザーを削除する（delete）
# def delete_user(db: Session, user_id: str):
#     # 指定されたユーザーIDに基づいてユーザーを削除
#     user = db.query(User).filter(User.id == user_id).first()
#     if user:
#         db.delete(user)
#         db.commit()
#     return user
