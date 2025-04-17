from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.db.session import get_db
from app import models
from app.schemas.table import *

router = APIRouter(prefix="/tables", tags=["tables"])


@router.post("/", response_model=TableRead)
def create_table(table: TableCreate, db: Session = Depends(get_db)):
    db_table = models.Table(**table.dict())
    db.add(db_table)
    db.commit()
    db.refresh(db_table)
    return db_table


@router.get("/", response_model=list[TableRead])
def read_tables(db: Session = Depends(get_db)):
    return db.query(models.Table).all()


@router.delete("/{table_id}")
def delete_table(table_id: int, db: Session = Depends(get_db)):
    table = db.query(models.Table).get(table_id)
    if not table:
        raise HTTPException(status_code=404, detail="Table not found")
    db.delete(table)
    db.commit()
    return {"detail": "Table deleted"}
