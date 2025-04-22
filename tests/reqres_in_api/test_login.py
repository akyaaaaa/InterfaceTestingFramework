from utils.concurrent_runner import run_concurrently
from utils.logger import log_info, log_error
from utils.test_runner import run_test_case, process_task


# def test_api(case, root_url):
#     run_test_case(case, root_url)
#
#
# def test_mul_api(all_test_cases, root_url):
#     process_task(all_test_cases, root_url)


def test_mul_api1(all_test_cases, root_url):
    # run_concurrently方法是把测试用例放入 多进程+多线程
    results = run_concurrently(all_test_cases, root_url)
    # 验证测试结果
    for result in results:
        assert result["status"] == "passed", f"Test failed: {result.get('message', '')}"
