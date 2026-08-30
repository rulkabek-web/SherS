from src.main.api.db.models.transaction_table import Transaction
from sqlalchemy.orm import Session

class TransactionCrudDb:
    @staticmethod
    def get_transactions_to_from_account_id(db: Session, from_account_id: int) -> Transaction | None:
        return db.query(Transaction).filter_by(from_account_id=from_account_id).first()


    @staticmethod
    def get_transactions_to_account_id(db: Session, to_account_id: int) -> Transaction | None:
        return db.query(Transaction).filter_by(to_account_id=to_account_id).first()

    @staticmethod
    def get_all_transactions_to_from_account_id(db: Session, from_account_id: int) -> Transaction | None:
        return db.query(Transaction).filter_by(from_account_id=from_account_id).all()