from sqlalchemy import create_engine

from config import conf

store = create_engine(conf.db, echo=True)

