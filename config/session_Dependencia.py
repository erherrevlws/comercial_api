from typing import Annotated
from fastapi import Depends
from sqlmodel import Session
from config.db import get_session

SessionDeDependencia = Annotated[Session, Depends(get_session)]