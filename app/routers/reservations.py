from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.db.session import get_db
from app.schemas.reservation import *
from app.services import reservation_service as reservation_service
from app import models

router = APIRouter(prefix="/reservations", tags=["reservations"])


@router.get("/", response_model=list[ReservationRead])
def get_reservations(db: Session = Depends(get_db)):
    return db.query(models.Reservation).all()


@router.post("/", response_model=ReservationRead)
def create_reservation(
        reservation: ReservationCreate,
        db: Session = Depends(get_db)
):
    return reservation_service.create_reservation(reservation, db)


@router.delete("/{reservation_id}")
def delete_reservation(reservation_id: int, db: Session = Depends(get_db)):
    reservation = db.query(models.Reservation).get(reservation_id)
    if not reservation:
        raise HTTPException(status_code=404, detail="Reservation not found")
    db.delete(reservation)
    db.commit()
    return {"detail": "Reservation deleted"}
