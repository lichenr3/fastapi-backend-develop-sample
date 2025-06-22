from sqlalchemy.orm import Session
from sqlalchemy import delete, desc, insert, select, update
from app.models.db_models import DeviceBaseInfos, FaceBaseInfos
from app.schemas.setting import DeviceBaseInfoRequest
from app.utils.constants import *


def query_marginal_device_info(session: Session):
    """
    获取设备信息
    :param session: 数据库会话
    :return: 设备信息列表
    """
    stmt = select(DeviceBaseInfos)
    result = session.execute(stmt).scalars().first()
    return result

def update_marginal_device_info(session: Session, request: DeviceBaseInfoRequest):
    update_data = {
        DEVICE_NAME: request.device_name,
        DEVICE_ADDRESS: request.device_address,
        COMMUNITY: request.community,
        PROJECT_NAME: request.project_name
    }
    stmt = update(DeviceBaseInfos).where(DeviceBaseInfos.id == 1).values(
        **update_data
    )
    result = session.execute(stmt)
    return result.rowcount > 0

def query_face_url(session: Session, id: int):
    stmt = select(FaceBaseInfos).where(FaceBaseInfos.id == id)
    result = session.execute(stmt).scalars().first()
    return result

def insert_face_data(session: Session, request: DeviceBaseInfoRequest, feature: list[float]):
    stmt = insert(FaceBaseInfos).values(
        face_name=request[FACE_NAME],
        face_img_url=request[FACE_IMAGE_URL],
        face_feature=feature
    )

    result = session.execute(stmt)
    return result.rowcount > 0

def update_face_data(session: Session, id: int, request: DeviceBaseInfoRequest, feature: list[float]):
    update_data = {
        FACE_NAME: request[FACE_NAME],
        FACE_IMAGE_URL: request[FACE_IMAGE_URL],
        FACE_FEATURE: feature
    }

    stmt = update(FaceBaseInfos).where(FaceBaseInfos.id == id).values(
        **update_data
    )
    result = session.execute(stmt)
    return result.rowcount > 0

def delete_face_data_by_id(session: Session, id: int) -> bool:
    stmt = delete(FaceBaseInfos).where(
    FaceBaseInfos.id == id
    )
    result = session.execute(stmt)
    return result.rowcount > 0

def query_face_info(
        session: Session,
        page: int,
        page_size: int,
        face_name: str
) -> list:
    stmt = (select(FaceBaseInfos))
    if face_name:
        stmt = stmt.where(FaceBaseInfos.face_name.like(f"%{face_name}%"))
    stmt = stmt.order_by(desc(FaceBaseInfos.create_time))
    stmt = stmt.offset((page - 1) * page_size).limit(page_size)
    return session.execute(stmt).scalars().all()
