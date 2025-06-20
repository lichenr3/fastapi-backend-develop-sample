
from sqlalchemy.orm import Session
from app.schemas.algorithms import *
from app.models.db_models import *
from app.crud.crud_algorithms import *
from app.schemas.common import OperatingResponse
from app.utils.exception_handler import *

def upload_algorithm_data_service(
        session: Session, request: AlgorithmCreateRequest
) -> OperatingResponse:
    try:
        result = insert_algorithm_by_data(
            session,
            request
        )

        if not result:
            raise ValueError("输入ID为非有效ID")
        session.commit()

    except Exception as e:
        session.rollback()
        raise e

    return OperatingResponse()

def modify_algorithm_data_service(
        session: Session,
        id: int,
        request: AlgorithmUpdateRequest
) -> OperatingResponse:
    try:
        result = update_algorithm_by_data(
            session,
            id,
            request
        )

        if not result:
            raise ValueError("输入ID为非有效ID")
        session.commit()

    except Exception as e:
        session.rollback()
        raise e

    return OperatingResponse()

def get_algorithms_info_service(
        session: Session,
        page: int,
        page_size: int,
        algorithm_name: str
) -> OperatingResponse:
    try:
        results = query_algorithm_by_name(session, page, page_size, algorithm_name)
        data = [AlgorithmBaseInfoResponse.model_validate(row) for row in results]

    except Exception as e:
        raise e

    return OperatingResponse(data=data)

def delete_algorithm_data_service(
        session: Session,
        id: int
) -> OperatingResponse:
    try:
        result = delete_algorithm_by_id(session, id)

        if not result:
            raise ValueError("输入ID为非有效ID")
        session.commit()

    except Exception as e:
        session.rollback()
        raise e

    return OperatingResponse

def modify_algorithm_status_service(
        session: Session,
        id: int,
        status: int
) -> OperatingResponse:
    try:
        if status not in [0, 1]:
            raise ValueError("输入错误: status_code只能为'0/1'")

        result = modify_algorithm_by_status(
            session,
            id,
            status
        )

        if not result:
            raise ValueError("输入ID为非有效ID")
        session.commit()

    except Exception as e:
        session.rollback()
        raise e

    return OperatingResponse()
