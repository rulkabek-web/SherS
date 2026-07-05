from src.main.api.db.models.credit_table import Credit
from sqlalchemy.orm import Session

class CreditCrudDb:
    @staticmethod
    def get_credit_by_id(db: Session, creditId: int) -> Credit | None:
        return db.query(Credit).filter_by(id=creditId).first()