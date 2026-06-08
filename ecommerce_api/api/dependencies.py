from typing import Annotated

from fastapi import Depends
from sqlalchemy.orm import Session

from ecommerce_api.infrastructure.database import get_db_session

DBSession = Annotated[Session, Depends(get_db_session)]
