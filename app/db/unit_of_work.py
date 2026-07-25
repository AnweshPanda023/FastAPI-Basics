from sqlalchemy.orm import Session


class UnitOfWork:

    def __init__(self, db: Session):
        self.db = db

    def __enter__(self):
        return self

    def __exit__(self, exc_type, exc_value, traceback):

        if exc_type is None:
            self.db.commit()
        else:
            self.db.rollback()

    def refresh(self, entity):
        self.db.refresh(entity)
