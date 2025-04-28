import concurrent.futures

from django.db import connection
from utils.test_runner import process_task
import django
import os

def init_django():
    # DJANGO_SETTINGS_MODULE 是 Django 的核心环境变量，用于指定项目的配置模块路径（此条指定backend.settings）
    os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'apps.backend.settings')
    django.setup()
    # 关闭并重新打开数据库连接
    if connection.connection:
        connection.close()

def run_concurrently(test_cases, num_processes=2):
    """
    使用多进程 + 多线程并发执行测试用例。
    :param test_cases: 测试用例列表
    :param root_url: 根 URL
    :param num_processes: 进程数
    :return: 所有测试用例的执行结果
    """
    # 初始化主进程Django环境
    init_django()
    
    # 将测试用例分成多个批次，每个批次分配给一个进程
    batch_size = len(test_cases) // num_processes
    batches = [
        test_cases[i : i + batch_size] for i in range(0, len(test_cases), batch_size)
    ]

    # 使用多进程执行
    all_results = []
    with concurrent.futures.ProcessPoolExecutor(
        max_workers=num_processes,
        initializer=init_django
    ) as executor:
        futures = [executor.submit(process_task, batch) for batch in batches]
        for future in concurrent.futures.as_completed(futures):
            all_results.extend(future.result())

    return all_results
