from typing import Annotated

from fastapi import Depends
from sqlalchemy.orm import Session

from ecommerce_api.infrastructure.database import get_db_session
from ecommerce_api.repositories.user_repo import UserRepository

DBSession = Annotated[Session, Depends(get_db_session)]


def get_user_repo(session: DBSession) -> UserRepository:
    return UserRepository(session)


UserRepo = Annotated[UserRepository, Depends(get_user_repo)]
