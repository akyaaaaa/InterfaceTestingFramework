# conftest.py
import os
import logging

# 定义日志目录
# 找到当前目录的父目录，也就是当前conftest.py的父目录InterfaceTestingFramework
PROJECT_ROOT = os.path.dirname(os.path.abspath(__file__))
LOG_DIR = os.path.join(PROJECT_ROOT, "logs")


if not os.path.exists(LOG_DIR):
    os.makedirs(LOG_DIR)

# 配置日志记录
logging.basicConfig(
    filename=os.path.join(LOG_DIR, "test.log"),  # 日志文件路径
    level=logging.INFO,  # 日志级别
    format="%(asctime)s - %(levelname)s - %(message)s",  # 日志格式
    encoding= "utf-8"
)

# 创建全局logger对象
logger = logging.getLogger(__name__)
