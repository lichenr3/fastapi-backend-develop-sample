
import traceback
import sys
from fastapi import APIRouter, Depends, Query, Body, Path, HTTPException
from sqlalchemy.orm import Session
from typing import Optional

from app.schemas.common import *
from app.schemas.algorithms import *
from app.services.algorithms_service import *
from app.api.deps import get_db

router = APIRouter()

@router.post("", response_model=OperatingResponse)
async def upload_algorithm_data(
        request: AlgorithmCreateRequest = Body(...),
        session: Session = Depends(get_db)
) -> OperatingResponse:
    try:
        return upload_algorithm_data_service(session, request)
    except HTTPException as http_exc:
        raise http_exc
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"服务器内部错误: {str(e)}")

@router.put("/{id}", response_model=OperatingResponse)
async def modify_algorithm_data(
        id: int,
        request: AlgorithmUpdateRequest = Body(...),
        session: Session = Depends(get_db)
) -> OperatingResponse:
    """
    更新设备信息
    session: 数据库会话
    request: 更新边缘设备信息请求体
    return: 基础信息响应对象
    """
    try:
        return modify_algorithm_data_service(session, id, request)
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"服务器内部错误: {str(e)}")

@router.get("", response_model=OperatingResponse)
async def get_algorithms_info(
        page: int = 1,
        page_size: int = 10,
        algorithm_name: str = '',
        session: Session = Depends(get_db)
) -> OperatingResponse:
    """
    获取设备信息
    :param request:
    :param session: 数据库会话
    :return: 边缘设备基础信息
    """
    try:
        return get_algorithms_info_service(
            session,
            page,
            page_size,
            algorithm_name
        )
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"服务器内部错误: {str(e)}")

@router.delete("/{id}", response_model=OperatingResponse)
async def delete_algorithm_data(
        id: int,
        session: Session = Depends(get_db)
) -> OperatingResponse:
    try:
        result = delete_algorithm_data_service(session, id)
        return result
    except ValueError as e:
        raise HTTPException(status_code=400, detail=f"查询参数错误: {str(e)}")
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"删除错误: {str(e)}")

@router.put("/{id}/status", response_model=OperatingResponse)
async def modify_algorithm_status(
        id: int,
        status: int,
        session: Session = Depends(get_db)
) -> OperatingResponse:
    try:
        result = modify_algorithm_status_service(session, id, status)
        return result
    except ValueError as e:
        raise HTTPException(status_code=400, detail=f"查询参数错误: {str(e)}")
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"更新错误: {str(e)}")
