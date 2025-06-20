
from pydantic import BaseModel, Field
from typing import Optional, TypeVar, Generic, List


class BaseModelStrip(BaseModel):
    """
    基础模型, 自动将所有空值转换为 None
    """
    def __init__(self, **data):
        data = {k: self._convert_empty_to_none(v) for k, v in data.items()}
        super().__init__(**data)

    @staticmethod
    def _convert_empty_to_none(value):
        if isinstance(value, dict):
            if not value:
                return None
            return {k: BaseModelStrip._convert_empty_to_none(v) for k, v in value.items()}
        elif isinstance(value, list):
            if not value:
                return None
            return [BaseModelStrip._convert_empty_to_none(v) for v in value]
        elif isinstance(value, str):
            if value == "":
                return None
            return value
        else:
            return value


TItem = TypeVar('TItem')

class BaseHeaderItemResponse(BaseModel):
    id: int = Field(0, description="ID")
    columnEn: str = Field("string", description="列英文名")
    columnCn: str = Field("string", description="列中文名")
    idx: int = Field(0, description="列索引")
    sort: int = Field(0, description="排序")
    visible: int = Field(0, description="是否可见")
    classType: str = Field("string", description="数据类型")
    lock: bool = Field(True, description="是否锁定")

class NestedDataPayload(BaseModel, Generic[TItem]):
    """
    嵌套的数据负载，包含列表数据及分页信息。
    """
    total: int = Field(..., description="总数")
    pageNum: int = Field(..., description="当前页码")
    pageSize: int = Field(..., description="每页大小")
    data: List[TItem] = Field(..., description="结果列表")
    header: Optional[List[BaseHeaderItemResponse]] = Field(None, description="表头信息列表")

class UnifiedResponse(BaseModel, Generic[TItem]):
    """
    统一的API响应结构。
    """
    code: int = Field(200, description="响应状态码")
    msg: str = Field(..., description="响应消息")
    data: NestedDataPayload[TItem] = Field(..., description="响应数据体")


# --- 简易响应对象 ---
class ItemInfoResponse(BaseModel, Generic[TItem]):
    """
    数据库个体查询响应模型
    """
    code: int = Field(200, description="状态码")
    message: str = Field("操作成功", description="响应信息")
    data: TItem = Field(..., description="响应数据体")


class OperatingResponse(BaseModel, Generic[TItem]):
    """
    数据库通用操作响应模型
    """
    code: int = Field(200, description="状态码")
    message: str = Field("操作成功", description="响应信息")
    data: List[TItem] = Field([], description="响应数据体")
