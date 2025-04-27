import requests
from django.conf import settings
from utils.logger import log_info, log_error

def run_test_case(test_case):
    """执行单个测试用例"""
    try:
        # 构建完整URL
        url = f"{test_case.root_url.rstrip('/')}/{test_case.url.lstrip('/')}"
        
        # 根据方法类型发送请求
        headers = {"x-api-key": "reqres-free-v1"}
        if test_case.method == 'GET':
            response = requests.get(url, headers=headers)
        elif test_case.method == 'POST':
            response = requests.post(url, json=test_case.body, headers=headers)
        elif test_case.method == 'PUT':
            response = requests.put(url, json=test_case.body, headers=headers)
        elif test_case.method == 'DELETE':
            response = requests.delete(url, headers=headers)
        else:
            raise ValueError(f"Unsupported HTTP method: {test_case.method}")
        
        # 验证响应状态码
        if response.status_code != test_case.expected_status_code:
            raise AssertionError(
                f"Expected status {test_case.expected_status_code}, got {response.status_code}"
            )
        
        # # 验证响应体（如果有预期值）
        # if test_case.expected_response and isinstance(test_case.expected_response, dict):
        #     response_json = response.json()
        #     for key, value in test_case.expected_response.items():
        #         if response_json.get(key) != value:
        #             raise AssertionError(
        #                 f"Field {key} mismatch. Expected {value}, got {response_json.get(key)}"
        #             )
        
        return {
            'status_code': response.status_code,
            'response': response.json(),
            'passed': True
        }
        
    except Exception as e:
        log_error(f"Test case {test_case.name} failed: {str(e)}")
        return {
            'error': str(e),
            'passed': False
        }
def process_task(test_cases, root_url):
    """批量执行测试用例"""
    results = []
    for case in test_cases:
        try:
            result = run_test_case(case)
            results.append({
                'id': case.id,
                'name': case.name,
                'status': 'success',
                'response': result
            })
        except Exception as e:
            results.append({
                'id': case.id,
                'name': case.name,
                'status': 'failed',
                'error': str(e)
            })
    return results
