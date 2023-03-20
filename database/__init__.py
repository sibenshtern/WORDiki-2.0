from sqlalchemy.orm import sessionmaker, Session, declarative_base
from sqlalchemy.engine import create_engine, Engine

SqlAlchemyBase = declarative_base()
__factory: Engine | None = None


def init(database_uri: str):
    global __factory

    if __factory:
        return

    if not database_uri.strip():
        raise FileNotFoundError("Specify database uri")
    connection_str = f"sqlite:///{database_uri.strip()}?check_same_thread=False"
    engine = create_engine(connection_str)
    __factory = sessionmaker(engine)

    from . import __all_models

    SqlAlchemyBase.metadata.create_all(engine)


def create_session() -> Session:
    if __factory is not None:
        return __factory()
    else:
        raise Exception("Database not initialized")


if __name__ == '__main__':
    pass
