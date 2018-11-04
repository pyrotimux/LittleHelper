from models import HelperTable
from database import db_session, engine, Base
from sqlalchemy.exc import IntegrityError
import sys
from werkzeug.local import LocalProxy
from flask import current_app as app
import traceback

_security = LocalProxy(lambda: app.extensions['security'])
_datastore = LocalProxy(lambda: _security.datastore)

class DbHelper():
    def dropdb(self):
        HelperTable.__table__.drop(engine)
        Base.metadata.create_all(bind=engine)

    def importdb(self, trans):
        with open(trans) as in_file:
            rows = in_file.read().strip().split("\n")

            for row in rows:
                items = row.split("||||")
                try:
                    db_session.add(HelperTable(items))
                    db_session.commit()
                except IntegrityError:
                    db_session.rollback()
                    