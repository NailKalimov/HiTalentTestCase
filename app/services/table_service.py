from sqlalchemy.orm import Session
from app.models.table import Table
from app.schemas.table import TableCreate, TableUpdate


def get_table(db: Session, table_id: int):
    return db.query(Table).filter(Table.id == table_id).first()


def get_tables(db: Session, skip: int = 0, limit: int = 100):
    return db.query(Table).offset(skip).limit(limit).all()


def create_table(db: Session, table: TableCreate):
    db_table = Table(**table.dict())
    db.add(db_table)
    db.commit()
    db.refresh(db_table)
    return db_table


def update_table(db: Session, table_id: int, table_data: TableUpdate):
    table = db.query(Table).filter(Table.id == table_id).first()
    if not table:
        return None
    for key, value in table_data.dict(exclude_unset=True).items():
        setattr(table, key, value)
    db.commit()
    db.refresh(table)
    return table


def delete_table(db: Session, table_id: int):
    table = db.query(Table).filter(Table.id == table_id).first()
    if table:
        db.delete(table)
        db.commit()
    return table
