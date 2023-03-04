import sqlalchemy    # нужно сделать ОРМ (замечание проверяющего №6)
import sqlalchemy as sq
from sqlalchemy.orm import declarative_base,  sessionmaker

Base = declarative_base()


class Users_orm(Base):
    __tablename__ = "users_orm"

    vk_id = sq.Column(sq.VARCHAR(length=50), primary_key=True)


def create_tables_orm(engine):
    Base.metadata.create_all(engine)


def drop_tables_orm(engine):
    Base.metadata.drop_all(engine)


def insert_data_orm(vk_id):
    person = Users_orm(vk_id=vk_id)
    session.add(person)
    session.commit()


def search_id_orm(vk_id):
    c = session.query(Users_orm).filter(Users_orm.vk_id == vk_id).count()
    session.commit()
    return c


DSN = "postgresql://postgres:1ngener@localhost:5432/postgres"
engine = sqlalchemy.create_engine(DSN)


Session = sessionmaker(bind=engine)
session = Session()
