from sqlalchemy.orm import Session


class UnitOfWork:

    def __init__(self, db: Session):
        self.db = db

    def __enter__(self):
        return self

    def __exit__(self, exc_type, exc_value, traceback):

        if exc_type is not None:
            self.db.rollback()
            return False

        try:
            self.db.commit()
        except Exception:
            self.db.rollback()
            raise

        return False

    def refresh(self, entity):
        self.db.refresh(entity)
