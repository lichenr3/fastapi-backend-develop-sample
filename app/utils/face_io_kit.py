
import os
import shutil
from deepface import DeepFace
from urllib.parse import urlparse
from app.utils.exception_handler import *
import cv2
import numpy as np
from fastapi import APIRouter, HTTPException, Depends, FastAPI, Form, File, UploadFile

def extract_face_features(image_url: str) -> list:
    """人脸特征提取封装"""
    try:
        if is_local_file(image_url):
            img = cv2.imread(image_url)
            if img is None:
                raise ImagePathValidationException("内部路径错误")
        result = DeepFace.represent(
            img_path=image_url,
            model_name="Facenet512",
            detector_backend="mtcnn"
        )
        return str(result[0]['embedding'])
    except ImagePathValidationException as e:
        raise e
    except Exception as e:
        raise FeatureExtractionException("人脸特征提取错误：" + str(e))

def save_face_image(face_name: str, image_file: UploadFile):
    """
    将指定图片保存到 face_repository/face_name/ 目录中。

    参数：
    - face_name: 人脸的名称（文件夹名）
    - image_path: 要保存的图片的本地路径
    """
    # 构造目标目录
    base_dir = "face_repository"
    save_dir = os.path.join(base_dir, face_name)

    # 创建目录，如果不存在
    os.makedirs(save_dir, exist_ok=True)

    # 获取原始图片文件名
    image_filename = image_file.filename

    # 构造完整保存路径
    save_path = os.path.join(save_dir, image_filename)

    # 复制图片到目标位置
    with open(save_path, "wb") as buffer:
        shutil.copyfileobj(image_file.file, buffer)

    return "./" + save_path

def is_url(path_or_url: str) -> bool:
    try:
        result = urlparse(path_or_url)
        return result.scheme in ("http", "https")
    except Exception:
        return False

def is_local_file(path_or_url: str) -> bool:
    return os.path.isfile(path_or_url)

def judge_image_source(path_or_url: str) -> str:
    """
    判断传入字符串是 URL 还是本地文件路径。
    返回:
    - "url" 表示图片 URL
    - "local_path" 表示本地文件路径
    - "unknown" 表示都不是
    """
    if is_url(path_or_url):
        return "url"
    elif is_local_file(path_or_url):
        return "local_path"
    else:
        return "unknown"

def delete_dir(image_path: str):
    dir_path = os.path.dirname(image_path)
    if os.path.exists(dir_path) and os.path.isdir(dir_path):
        shutil.rmtree(dir_path)
        print(f"已删除整个文件夹：{dir_path}")
    else:
        print(f"路径不存在或不是文件夹：{dir_path}")
