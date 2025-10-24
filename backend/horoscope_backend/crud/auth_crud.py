from typing import Optional

from passlib.context import CryptContext
from sqlalchemy.orm import Session

from ..models.user import User

# Use argon2 instead of bcrypt to avoid the 72-byte limit issue
pwd_context = CryptContext(schemes=["argon2"], deprecated="auto")


def verify_password(plain_password: str, hashed_password: str) -> bool:
    try:
        return pwd_context.verify(plain_password, hashed_password)
    except ValueError as e:
        # Handle bcrypt errors
        print(f"Password verification error: {e}")
        return False


def get_password_hash(password: str) -> str:
    try:
        # Ensure password is a string and truncate if necessary
        if not isinstance(password, str):
            password = str(password)

        # Truncate to 72 characters if necessary (bcrypt limit)
        if len(password) > 72:
            password = password[:72]

        return pwd_context.hash(password)
    except Exception as e:
        print(f"Password hashing error: {e}")
        raise


def get_user_by_id(db: Session, user_id: int) -> Optional[User]:
    return db.query(User).filter(User.id == user_id).first()


def get_user_by_username(db: Session, username: str) -> Optional[User]:
    return db.query(User).filter(User.username == username).first()


def get_user_by_email(db: Session, email: str) -> Optional[User]:
    return db.query(User).filter(User.email == email).first()


def create_user(db: Session, username: str, email: str, password: str) -> User:
    hashed_password = get_password_hash(password)
    user = User(username=username, email=email, hashed_password=hashed_password)
    db.add(user)
    db.commit()
    db.refresh(user)
    return user


def authenticate_user(db: Session, username: str, password: str) -> Optional[User]:
    user = get_user_by_username(db, username)
    if not user:
        return None
    if not verify_password(password, user.hashed_password):
        return None
    return user
