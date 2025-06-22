
from sqlalchemy import (
    Column,
    Integer,
    String,
    Float,
    Text,
    DateTime,
    ForeignKey,
    func
)
from sqlalchemy.orm import relationship, declarative_base

Base = declarative_base()

class CameraBaseInfo(Base):
    """
    摄像头注册基础信息表
    """
    __tablename__ = 'camera_base_infos'

    # === 列定义 ===
    id = Column(Integer, primary_key=True, autoincrement=True)
    camera_username = Column(String(50), nullable=True, comment='摄像头登录用户名')
    camera_password = Column(String(50), nullable=True, comment='摄像头登录密码')
    camera_factory = Column(Integer, nullable=True, comment='摄像头厂商: 0-海康，1-大华，2-宇视')
    camera_ip = Column(String(20), nullable=True, comment='摄像头内网ip地址')
    camera_address = Column(String(50), nullable=True, comment='摄像头所在小区内的地址')
    status = Column(Integer, nullable=True, comment='摄像头状态：0-离线，1-在线')
    offline_time = Column(DateTime, nullable=True, comment='离线时间记录')

    # 使用 server_default 和 onupdate 来让数据库本身处理时间戳的创建和更新
    create_time = Column(
        DateTime,
        nullable=False,
        server_default=func.now(),
        onupdate=func.now(),
        comment='数据创建时间'
    )

    # === 关系定义 ===
    # 定义与 TaskBaseInfo 的反向关系
    # 允许通过 camera.tasks 访问一个摄像头下的所有任务
    tasks = relationship("TaskBaseInfo", back_populates="camera")

    # 定义表的元数据
    __table_args__ = {
        'comment': '摄像头注册基础信息表'
    }

    # 调试用: 重写 __repr__ 方法, 打印该对象时将按照改写后的格式输出
    def __repr__(self):
        return f"<CameraBaseInfo(id={self.id}, camera_ip='{self.camera_ip}', status={self.status})>"

class AlgorithmBaseInfos(Base):
    """
    算法基础信息表
    """
    __tablename__ = 'algorithm_base_infos'

    # === 列定义 ===
    id = Column(Integer, primary_key=True, autoincrement=True)
    algorithm_name = Column(String(50), nullable=True, comment='算法名称')
    algorithm_version = Column(String(50), nullable=True, comment='算法版本')
    algorithm_capacity = Column(String(100), nullable=True, comment='算法能力说明')
    algorithm_status = Column(Integer, nullable=True, comment='算法运行状态：0-停止、1-运行')

    create_time = Column(
        DateTime,
        nullable=False,
        server_default=func.now(),
        onupdate=func.now(),
        comment='数据创建时间'
    )

    # === 关系定义 ===
    tasks = relationship("TaskBaseInfo", back_populates="algorithm")

    __table_args__ = {
        'comment': '算法基础信息表'
    }

    def __repr__(self):
        return f"<AlgorithmBaseInfo(id={self.id}, name='{self.algorithm_name}', version='{self.algorithm_version}')>"

class TaskBaseInfo(Base):
    """
    检测任务信息表
    """
    __tablename__ = 'task_base_infos'

    # === 列定义 ===
    id = Column(Integer, primary_key=True, autoincrement=True)
    task_name = Column(String(50), nullable=True, comment='任务名称')

    algorithm_id = Column(Integer, ForeignKey('algorithm_base_infos.id', ondelete='NO ACTION'), comment='算法基础信息表的id值')
    camera_id = Column(Integer, ForeignKey('camera_base_infos.id', ondelete='NO ACTION'), comment='摄像头id值')

    camera_detect_range = Column(String(50), nullable=True, comment='多边形检测范围点数据')
    detect_frequency = Column(Integer, nullable=True, comment='检查频率：一分钟检测多少次')
    warn_url = Column(String(255), nullable=True, comment='预警检测上报接口')
    detect_threshold = Column(Float, nullable=True, comment='算法检测的阈值分数')
    status = Column(Integer, nullable=True, comment='任务状态：0-停止、1-运行')

    create_time = Column(
        DateTime,
        nullable=False,
        server_default=func.now(),
        onupdate=func.now(),
        comment='数据创建时间'
    )

    # === 关系定义 ===
    algorithm = relationship("AlgorithmBaseInfos", back_populates="tasks")
    camera = relationship("CameraBaseInfo", back_populates="tasks")

    __table_args__ = {
        'comment': '检测任务信息表'
    }

    def __repr__(self):
        return f"<TaskBaseInfo(id={self.id}, task_name='{self.task_name}', status={self.status})>"

class DeviceBaseInfos(Base):
    """
    边缘设备基础信息表
    """
    __tablename__ = 'device_base_infos'

    # === 列定义 ===
    id = Column(Integer, primary_key=True, autoincrement=True)
    device_name = Column(String(50), nullable=True, comment='边缘设备名称')
    device_address = Column(String(50), nullable=True, comment='部署地址')
    community = Column(String(50), nullable=True, comment='部署小区')
    project_name = Column(String(50), nullable=True, comment='项目名称')

    create_time = Column(
        DateTime,
        nullable=False,
        server_default=func.now(),
        onupdate=func.now(),
        comment='数据创建时间'
    )

    __table_args__ = {
        'comment': '边缘设备基础信息表'
    }

    def __repr__(self):
        return f"<DeviceBaseInfos(id={self.id}, device_name='{self.device_name}', project_name='{self.project_name}')>"

class FaceBaseInfos(Base):
    """
    人脸数据基础信息表
    """
    __tablename__ = 'face_base_infos'

    # === 列定义 ===
    id = Column(Integer, primary_key=True, autoincrement=True)
    face_name = Column(String(50), nullable=True, comment='人脸名称')
    face_img_url = Column(String(100), nullable=True, comment='人脸图像URL')
    face_feature = Column(Text, nullable=True, comment='人脸特征向量')

    create_time = Column(
        DateTime,
        nullable=False,
        server_default=func.now(),
        onupdate=func.now(),
        comment='数据创建时间'
    )

    __table_args__ = {
        'comment': '人脸数据基础信息表'
    }

    def __repr__(self):
        return f"<FaceBaseInfos(id={self.id}, face_name='{self.face_name}')>"
