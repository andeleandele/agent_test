from sqlalchemy.orm import Session
from models.users import User as UserModel
from schemas.user import UserCreate

  

def get_user(db: Session, user_id: int):
    return db.query(UserModel).filter(UserModel.id == user_id).first()

def create_user(db: Session, user: UserCreate):
    db_user = UserModel(name=user.name, email=user.email)
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    return db_user

def delete_user(db: Session, user_id: int):
    db_user = db.query(UserModel).filter(UserModel.id == user_id).first()
    if db_user:
        db.delete(db_user)
        db.commit()
    return db_user

# TODO: Users should be deleted from DB (not just deactivated)

def get_all_users(db: Session):
    return db.query(UserModel).all()

