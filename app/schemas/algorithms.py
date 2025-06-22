
from pydantic import BaseModel, Field
from typing import Optional
from datetime import datetime

class AlgorithmBase(BaseModel):
    """
    算法的基础字段模型
    """
    algorithm_name: Optional[str] = Field(None, description="算法名称")
    algorithm_version: Optional[str] = Field(None, description="算法版本")
    algorithm_capacity: Optional[str] = Field(None, description="算法能力说明")

class AlgorithmCreateRequest(AlgorithmBase):
    """
    新增算法数据请求体
    """
    algorithm_name: str = Field(..., description="算法名称")
    algorithm_version: str = Field(..., description="算法版本")
    algorithm_capacity: str = Field(..., description="算法能力说明")

class AlgorithmUpdateRequest(AlgorithmBase):
    """
    更新算法数据请求体
    """
    pass

class AlgorithmBaseInfo(AlgorithmBase):
    id: int = Field(..., description="算法名称")
    algorithm_status: int = Field(..., description="算法运行状态")
    create_time: datetime = Field(..., description="数据创建时间")

    class Config:
        from_attributes = True
