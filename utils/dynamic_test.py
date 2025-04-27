import requests

from utils.logger import log_info, log_error


class DynamicTest:
    # 可以使用--category参数来指定跑具体模块的用例
    @staticmethod
    def dynamic_tests_category(test_case, root_url):
        log_info(f"正在运行用例: {test_case['name']}")
        # 构造请求
        method = test_case["method"]
        url = root_url + test_case["url"]
        body = test_case["body"]
        try:
            # 加上demo网站的特殊headers，不然可能请求错误
            headers = {"x-api-key": "reqres-free-v1"}
            if method == "GET":
                response = requests.get(url, headers=headers)
            elif method == "POST":
                response = requests.post(url, json=body, headers=headers)
            elif method == "PUT":
                response = requests.put(url, json=body, headers=headers)
            elif method == "PATCH":
                response = requests.patch(url, json=body, headers=headers)
            elif method == "DELETE":
                response = requests.delete(url, headers=headers)
            else:
                assert False, f"Unsupported method: {method}"

            # 检查状态码
            assert response.status_code == test_case["expected_status_code"], (
                f"Status code mismatch. Expected: {test_case['expected_status_code']}",
                f"Got: {response.status_code}",
            )

            # # 检查响应内容
            # try:
            #     actual_response = response.json()
            #     expected_response = test_case["expected_response"]
            #
            #     assert actual_response == expected_response, (
            #         f"Response content mismatch.\nExpected: {json.dumps(expected_response, indent=2)}\nGot: {json.dumps(actual_response, indent=2)}",
            #         "Failed to parse response as JSON."
            #     )
            # except Exception as e:
            #     log_error(f"Request failed with error: {e}")
            #     raise
        except Exception as e:
            log_error(f"Request failed with error: {e}")
            raise
