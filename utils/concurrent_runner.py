import concurrent.futures
from utils.test_runner import process_task


def run_concurrently(test_cases, root_url, num_processes=3):
    """
    使用多进程 + 多线程并发执行测试用例。
    :param test_cases: 测试用例列表
    :param root_url: 根 URL
    :param num_processes: 进程数
    :return: 所有测试用例的执行结果
    """
    # 将测试用例分成多个批次，每个批次分配给一个进程
    batch_size = len(test_cases) // num_processes
    batches = [test_cases[i:i + batch_size] for i in range(0, len(test_cases), batch_size)]

    # 使用多进程执行
    all_results = []
    with concurrent.futures.ProcessPoolExecutor(max_workers=num_processes) as executor:
        futures = [executor.submit(process_task, batch, root_url) for batch in batches]
        for future in concurrent.futures.as_completed(futures):
            all_results.extend(future.result())

    return all_results
