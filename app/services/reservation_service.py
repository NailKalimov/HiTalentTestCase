from datetime import datetime, timedelta
from sqlalchemy.orm import Session
from app import models
from fastapi import HTTPException

from app.models import Reservation
from app.schemas.reservation import *


def is_table_available(
        db: Session,
        table_id: int,
        reservation_time: datetime,
        duration_minutes: int
) -> bool:
    end_time = reservation_time + timedelta(minutes=duration_minutes)

    reservations = (
        db.query(models.Reservation)
        .filter(models.Reservation.table_id == table_id)
        .all()
    )

    for r in reservations:
        r_start = r.reservation_time
        r_end = r_start + timedelta(minutes=r.duration_minutes)
        # Проверка на пересечение
        if reservation_time < r_end and end_time > r_start:
            return False

    return True


def create_reservation(reservation: ReservationCreate, db: Session) -> Reservation:
    try:
        r_start = reservation.reservation_time
        r_end = r_start + timedelta(minutes=reservation.duration_minutes)

        existing_reservations = db.query(Reservation).filter(
            Reservation.table_id == reservation.table_id
        ).all()

        for existing in existing_reservations:
            e_start = existing.reservation_time
            e_end = e_start + timedelta(minutes=existing.duration_minutes)

            if r_start < e_end and r_end > e_start:
                raise HTTPException(
                    status_code=400,
                    detail="Table is already reserved for the selected time slot.",
                )

        new_reservation = Reservation(**reservation.dict())
        db.add(new_reservation)
        db.commit()
        db.refresh(new_reservation)
        return new_reservation

    except HTTPException as e:
        raise

    except Exception as e:
        print("💥 Ошибка при создании брони:", e)
        raise HTTPException(status_code=500, detail=str(e))
