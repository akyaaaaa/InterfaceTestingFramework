import os
import logging
from logging.handlers import RotatingFileHandler

# 定义日志目录
PROJECT_ROOT = os.path.dirname(os.path.abspath(__file__))  # 当前 conftest.py 所在目录
LOG_DIR = os.path.join(PROJECT_ROOT, "logs")

# 确保日志目录存在
if not os.path.exists(LOG_DIR):
    os.makedirs(LOG_DIR)


# 配置日志记录
def setup_logger():
    # 创建 logger 对象
    logger = logging.getLogger("test_logger")
    logger.setLevel(logging.INFO)  # 设置日志级别为 INFO

    # 创建文件处理器（支持日志轮转）
    file_handler = RotatingFileHandler(
        os.path.join(LOG_DIR, "test.log"),
        maxBytes=10 * 1024 * 1024,  # 每个日志文件最大 10MB
        backupCount=5,  # 保留最多 5 个备份文件
        encoding="utf-8",
    )
    file_handler.setLevel(logging.INFO)

    # 创建控制台处理器
    console_handler = logging.StreamHandler()
    console_handler.setLevel(logging.INFO)

    # 设置日志格式
    formatter = logging.Formatter("%(asctime)s - %(levelname)s - %(message)s")
    file_handler.setFormatter(formatter)
    console_handler.setFormatter(formatter)

    # 将处理器添加到 logger
    logger.addHandler(file_handler)
    logger.addHandler(console_handler)

    return logger


# 初始化全局 logger 对象
logger = setup_logger()
