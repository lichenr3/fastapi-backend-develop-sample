
from sqlalchemy import select, desc
from datetime import datetime
from sqlalchemy.orm import Session
from sqlalchemy import delete, desc, insert, select, update
from app.models.db_models import AlgorithmBaseInfos
from app.schemas.algorithms import *
from app.utils.constants import *

def insert_algorithm_by_data(
        session: Session,
        request: AlgorithmCreateRequest
) -> bool:
    insert_data = request.model_dump()
    insert_data["algorithm_status"] = 0
    stmt = insert(AlgorithmBaseInfos).values(**insert_data)
    result = session.execute(stmt)
    return result.rowcount > 0

def update_algorithm_by_data(
        session: Session,
        id: int,
        request: AlgorithmUpdateRequest
) -> bool:
    update_data = request.model_dump(exclude_unset=True)

    stmt = (
        update(AlgorithmBaseInfos)
        .where(AlgorithmBaseInfos.id == id)
        .values(**update_data)
    )
    result = session.execute(stmt)
    return result.rowcount > 0

def query_algorithm_by_name(
        session: Session,
        page: int,
        page_size: int,
        algorithm_name: str
) -> list:
    stmt = (
        select(AlgorithmBaseInfos)
    )

    if algorithm_name:
        stmt = stmt.where(AlgorithmBaseInfos.algorithm_name.like(f"%{algorithm_name}%"))

    stmt = stmt.order_by(desc(AlgorithmBaseInfos.create_time))
    stmt = stmt.offset((page - 1) * page_size).limit(page_size)
    result = session.execute(stmt).scalars().all()

    return result if result else []

def delete_algorithm_by_id(
        session: Session,
        id: int
) -> bool:
    stmt = delete(AlgorithmBaseInfos).where(
        AlgorithmBaseInfos.id == id
    )
    result = session.execute(stmt)
    return result.rowcount > 0

def modify_algorithm_by_status(
        session: Session,
        id: int,
        status: int
) -> bool:
    stmt = update(AlgorithmBaseInfos).values(
        algorithm_status=status).where(
        AlgorithmBaseInfos.id == id
    )
    result = session.execute(stmt)
    return result.rowcount > 0
