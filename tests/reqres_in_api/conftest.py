import json
import uuid
from typing import Iterable

import pytest

from utils.data_loader import load_json
from utils.dynamic_test import DynamicTest
from utils.logger import log_info, log_error


def pytest_addoption(parser):
    parser.addoption(
        "--category",
        action="store",
        default="all",
        help="Run test cases of a specific category (e.g., reqres_in_api, user, resource)",
    )


# 动态生成测试用例的 Collector 类
def create_test_function(case, root_url):
    # 把遍历的case传入到test_login.Test_login.dynamic_tests_login(case)方法
    return lambda: DynamicTest.dynamic_tests_category(case, root_url)


class CategoryTestsCollector(pytest.Collector):
    # 根据json动态生成用例
    def collect(self) -> Iterable[pytest.Item | pytest.Collector]:
        try:
            # 获取命令行参数
            category = self.config.getoption("--category")
            # 加载 JSON 数据
            test_data = load_json(
                file_name="example_data.json", modelname="reqres_in_api"
            )
            root_url = test_data.get("ROOTURL")
            # 如果test_data中没有"test_cases"键，代码不会抛出异常，而是返回一个空列表[]
            test_cases = test_data.get("test_cases", [])

            if not root_url:
                raise ValueError("Missing 'ROOTURL' in the test data.")
            # 根据标记筛选用例
            if category == "all":
                filtered_cases = test_cases  # 运行所有用例
            else:
                filtered_cases = [
                    case for case in test_cases if case.get("category") == category
                ]

            for index, case in enumerate(filtered_cases):
                # 筛选与登录相关的测试用例
                yield pytest.Function.from_parent(
                    self,
                    # name=f"{case['name']}_{uuid.uuid4().hex[:6]}",
                    name=f"{case['name']}_{index}",
                    callobj=create_test_function(case, root_url),
                )
        except Exception as e:
            print(f"Failed to load test cases: {e}")


def pytest_pycollect_makeitem(collector, name, obj):
    # 如果方法名是dynamic_tests_login，则动态生成用例
    # if name == 'dynamic_tests_category':
    #     return CategoryTestsCollector.from_parent(collector, name=name)
    ...


# 动态生成测试函数
def pytest_generate_tests(metafunc):
    if "case" in metafunc.fixturenames:
        test_data = load_json("example_data.json", modelname="reqres_in_api")
        test_cases = test_data.get("test_cases", [])
        metafunc.parametrize("case", test_cases)


@pytest.fixture(scope="session")
def all_test_cases():
    """加载所有测试用例"""
    test_data = load_json("example_data.json", modelname="reqres_in_api")
    return test_data.get("test_cases", [])


@pytest.fixture(scope="session")
def root_url():
    """加载根 URL"""
    test_data = load_json("example_data.json", modelname="reqres_in_api")
    return test_data.get("ROOTURL")
