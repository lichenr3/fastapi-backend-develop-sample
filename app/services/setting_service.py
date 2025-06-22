
from app.schemas.common import *
from app.schemas.setting import *
from app.crud.crud_setting import *
from app.utils.face_io_kit import *
from app.utils.constants import *
from app.utils.face_io_kit import judge_image_source


def get_device_info_service(session: Session) -> ItemInfoResponse:
    """
    获取设备信息
    :param session: 数据库会话
    :return: 设备信息列表
    """
    try:
        device_info = query_marginal_device_info(session)
        response_info = DeviceBaseInfoResponse.model_validate(device_info)

        return ItemInfoResponse(data=response_info)
    except Exception as e:
        raise DatabaseException(f"获取设备信息失败: {str(e)}")

def update_device_info_service(session: Session, request: DeviceBaseInfoRequest) -> OperatingResponse:
    try:
        result = update_marginal_device_info(session, request)
        session.commit()
        if result:
            return OperatingResponse()
        else:
            raise DatabaseException(f"数据库更新动作报错: {str(e)}")
    except DatabaseException as e:
        session.rollback()
        raise e
    except Exception as e:
        session.rollback()
        raise e

def upload_face_data_service(session: Session, request: dict) -> OperatingResponse:
    try:
        if request[FACE_IMAGE_URL]:
            embedding = extract_face_features(request[FACE_IMAGE_URL])
            result = insert_face_data(session, request, embedding)
            session.commit()
        elif request[LOCAL_IMAGE]:
            save_path = save_face_image(request[FACE_NAME], request[LOCAL_IMAGE])
            embedding = extract_face_features(save_path)
            request[FACE_IMAGE_URL] = save_path
            result = insert_face_data(session, request, embedding)
            session.commit()
        else:
            raise NotImplementedError("未提供有效的图像输入")
        if not result:
            raise DataValidationException("输入ID为非有效ID")
        return OperatingResponse()
    except FeatureExtractionException as e:
        session.rollback()
        raise e
    except ValueError as e:
        session.rollback()
        raise DataValidationException("输入图片内容错误：无法提取特征", str(e))
    except DatabaseException as e:
        session.rollback()
        raise e
    except Exception as e:
        session.rollback()
        raise e

def modify_face_data_service(session: Session, id: int, request: dict) -> OperatingResponse:
    try:
        pre_detect = query_face_url(session, id)
        if not pre_detect:
            raise DataValidationException("输入ID为非有效ID")
        strategy = judge_image_source(pre_detect.face_img_url)

        # 获取原始图像路径（用于本地图片清理）
        if strategy == "local_path":
            image_path = pre_detect.face_img_url
            delete_dir(image_path)

        # 图像来源判定 + 特征提取
        if request[FACE_IMAGE_URL]:
            embedding = extract_face_features(request[FACE_IMAGE_URL])
        elif request[LOCAL_IMAGE]:
            save_path = save_face_image(request[FACE_NAME], request[LOCAL_IMAGE])
            embedding = extract_face_features(save_path)
            request[FACE_IMAGE_URL] = save_path
        else:
            raise NotImplementedError("未提供有效的图像输入")

        # 更新数据库
        update_face_data(session, id, request, embedding)

        session.commit()
        return OperatingResponse()

    except FeatureExtractionException as e:
        session.rollback()
        raise e
    except ValueError as e:
        session.rollback()
        raise DataValidationException("输入图片内容错误：无法提取特征", str(e))
    except DatabaseException as e:
        session.rollback()
        raise e
    except NotImplementedError as e:
        raise e
    except Exception as e:
        session.rollback()
        raise e

def delete_face_data_service(session: Session, id: int) -> OperatingResponse:
    try:
        if_delete = False
        image_path = ''
        pre_detect = query_face_url(session, id)
        if not pre_detect:
            raise DataValidationException("输入ID为非有效ID")
        if judge_image_source(pre_detect.face_img_url) == "local_path":
            if_delete = True
            image_path = pre_detect.face_img_url
        delete_face_data_by_id(session, id)
        session.commit()

        if if_delete:
            delete_dir(image_path)

        return OperatingResponse()
    except DataValidationException as e:
        raise e
    except Exception as e:
        session.rollback()
        raise e

def get_face_service(
        session: Session,
        page: int,
        page_size: int,
        face_name: str
) -> OperatingResponse:
    try:
        result = query_face_info(session, page, page_size, face_name)
        session.commit()
        intend_output = []

        for row in result:
            unit_data = FaceIdentityBaseInfo(
                id=row.id,
                image=row.face_img_url,
                face_name=row.face_name,
            )
            intend_output.append(unit_data)

        return OperatingResponse(data=intend_output)

    except Exception as e:
        session.rollback()
        raise e
