
import traceback
import sys
from fastapi import APIRouter, HTTPException, UploadFile, Depends, Form, File, Body
from sqlalchemy.orm import Session
from app.api.deps import get_db
from app.services.setting_service import *
from app.schemas.common import *
from app.schemas.setting import *

router = APIRouter()

@router.get("/device", response_model=ItemInfoResponse)
async def get_device_info(session: Session = Depends(get_db)) -> ItemInfoResponse:
    """
    获取设备信息
    :param session: 数据库会话
    :return: 边缘设备基础信息
    """
    try:
        return get_device_info_service(session)
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"{str(e)}")

@router.put("/device/{id}", response_model=OperatingResponse)
async def update_device_info(request: DeviceBaseInfoRequest = Body(...), session: Session = Depends(get_db)) -> OperatingResponse:
    """
    更新设备信息
    session: 数据库会话
    request: 更新边缘设备信息请求体
    return: 基础信息响应对象
    """
    try:
        return update_device_info_service(session, request)
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"{str(e)}")

@router.post("/face_data", response_model=OperatingResponse)
async def upload_face_data(
        face_name: str = Form(...),
        face_img_url: str = Form(None),
        local_image: UploadFile | None = File(default=None),
        session: Session = Depends(get_db)
) -> OperatingResponse:
    try:
        if face_img_url and local_image:
            raise HTTPException(
                status_code=422, detail="face_img_url 和 local_image 不应同时提供"
            )
        elif not local_image and not face_img_url:
            raise HTTPException(
                status_code=422, detail="face_img_url 和 local_image 至少需要提供一个"
            )
        request = {
            "face_name": face_name,
            "face_img_url": face_img_url if face_img_url else None,
            "local_image": local_image if local_image else None
        }
        return upload_face_data_service(session, request)
    except HTTPException as http_exc:
        raise http_exc
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"服务器内部错误: {str(e)}")

@router.put("/face_data/{id}", response_model=OperatingResponse)
async def modify_face_data(
        id: int,
        face_name: str = Form(...),
        face_img_url: str = Form(None),
        local_image: UploadFile = File(None),
        session: Session = Depends(get_db)
) -> OperatingResponse:
    try:
        if face_img_url and local_image:
            raise HTTPException(
                status_code=422, detail="face_img_url 和 local_image 不应同时提供"
            )
        elif not local_image and not face_img_url:
            raise HTTPException(
                status_code=422, detail="face_img_url 和 local_image 至少需要提供一个"
            )
        request = {
            "face_name": face_name,
            "face_img_url": face_img_url if face_img_url else None,
            "local_image": local_image if local_image else None
        }
        return modify_face_data_service(session, id, request)
    except Exception as e:
        tb_str = ''.join(traceback.format_exception(type(e), e, e.__traceback__))
        print(f"[ERROR] Exception occurred:\n{tb_str}", file=sys.stderr)  # 打印带文件名/行号的堆栈
        raise HTTPException(status_code=500, detail=f"{str(e)}")

@router.delete("/face/{id}", response_model=OperatingResponse)
async def delete_face_data(
        id: int,
        session: Session = Depends(get_db)
) -> OperatingResponse:
    try:
        return delete_face_data_service(session, id)
    except Exception as e:
        tb_str = ''.join(traceback.format_exception(type(e), e, e.__traceback__))
        print(f"[ERROR] Exception occurred:\n{tb_str}", file=sys.stderr)  # 打印带文件名/行号的堆栈
        raise HTTPException(status_code=500, detail=f"{str(e)}")

@router.get("/face", response_model=OperatingResponse)
async def get_face_info(
        page: int = 1,
        page_size: int = 10,
        face_name: str = '',
        session: Session = Depends(get_db)
) -> OperatingResponse:
    try:
        return get_face_service(session, page, page_size, face_name)
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"{str(e)}")
