# 执行单个测试用例
import concurrent.futures

from utils.dynamic_test import DynamicTest


def run_test_case(case, root_url):
    try:
        DynamicTest.dynamic_tests_category(case, root_url)
        return {"name": case["name"], "status": "passed"}
    except Exception as e:
        return {"name": case["name"], "status": "failed", "message": str(e)}


# 在一个进程中并发执行一批测试用例,多线程
def process_task(test_cases, root_url):
    results = []
    with concurrent.futures.ThreadPoolExecutor(
        max_workers=3
    ) as executor:  # 每个进程使用 4 个线程
        futures = [
            executor.submit(run_test_case, case, root_url) for case in test_cases
        ]
        for future in concurrent.futures.as_completed(futures):
            results.append(future.result())
    return results
