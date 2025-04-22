import pytest
from utils.logger import log_info, log_error


def main():
    log_info("Running pytest for formal testing...")
    pytest.main(["-v", "-s"])  # 使用 `-v` 参数显示详细输出


if __name__ == "__main__":
    main()
