
from pydantic import BaseModel, Field
from typing import Optional
from app.models.db_models import *

class DeviceBase(BaseModel):
    """
    系统设置基础字段模型
    """
    device_name: Optional[str] = Field(..., description="边缘设备名称")
    device_address: Optional[str] = Field(..., description="部署地址")
    community: Optional[str] = Field(..., description="部署小区")
    project_name: Optional[str] = Field(..., description="项目名称")

class DeviceBaseInfoRequest(DeviceBase):
    """
    边缘设备的基础字段模型请求对象
    """
    pass

class DeviceBaseInfoResponse(DeviceBase):
    """
    边缘设备的基础字段模型响应对象
    """
    class Config:
        from_attributes = True

class FaceIdentityBaseInfo(BaseModel):
    id: int = Field(..., description="人脸id")
    image: str = Field(..., description="人脸图片")
    face_name: str = Field(..., description="人脸名称")

    class Config:
        from_attributes = True
