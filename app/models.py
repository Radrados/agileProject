from typing import Optional
import sqlalchemy as sql_al
import sqlalchemy.orm as sql_orm
from app import db

class User(db.Model):
    id: sql_orm.Mapped[int] = sql_orm.mapped_column(primary_key=True)
    first_name: sql_orm.Mapped[str] = sql_orm.mapped_column(sql_al.String(32), index=True)
    last_name: sql_orm.Mapped[str] = sql_orm.mapped_column(sql_al.String(32), index=True)
    email: sql_orm.Mapped[str] = sql_orm.mapped_column(sql_al.String(120), index=True, unique=True)
    password_hash: sql_orm.Mapped[Optional[str]] = sql_orm.mapped_column(sql_al.String(256))

    # prints object of this class --> debuging 
    def __repr__(self):
        return '<User {}>'.format(self.email)