# -*- coding: utf-8 -*-
"""测试数据生成工具

提供测试中常用的Mock数据生成器，包括Response对象、时间值等。
确保测试数据的一致性和可维护性。

使用 tests.test_data_generator示例:

    # 创建成功响应
    success_response = ResponseFactory.success()

    # 创建标准时间序列
    time_values = TimeFactory.standard()
"""

from datetime import timedelta
from unittest.mock import MagicMock
import requests


class ResponseFactory:
    """Response对象工厂类

    用于创建模拟的requests.Response对象，支持各种状态和场景。
    """

    @staticmethod
    def success(content: bytes = b'Success', elapsed_ms: int = 100) -> MagicMock:
        """创建成功响应(200 OK)

        Args:
            content: 响应内容，默认为b'Success'
            elapsed_ms: 响应时间(毫秒)，默认为100ms

        Returns:
            MagicMock: 模拟的Response对象
        """
        response = MagicMock(spec=requests.Response)
        response.status_code = 200
        response.content = content
        response.elapsed = timedelta(milliseconds=elapsed_ms)
        response.headers = {
            'Content-Type': 'text/html; charset=utf-8',
            'Content-Length': str(len(content))
        }
        response.text = content.decode('utf-8', errors='ignore')
        response.ok = True
        response.raise_for_status = MagicMock(return_value=None)
        return response

    @staticmethod
    def timeout(elapsed_seconds: int = 30) -> MagicMock:
        """创建超时响应

        用于模拟请求超时场景，通常响应时间超过阈值。

        Args:
            elapsed_seconds: 超时时间(秒)，默认为30秒

        Returns:
            MagicMock: 模拟的超时Response对象
        """
        response = MagicMock(spec=requests.Response)
        response.status_code = 200  # 超时通常在响应前发生
        response.elapsed = timedelta(seconds=elapsed_seconds)
        response.content = b'Timeout'
        response.headers = {}
        return response

    @staticmethod
    def error(status_code: int, message: str = 'Error', elapsed_ms: int = 50) -> MagicMock:
        """创建HTTP错误响应

        用于模拟各种HTTP错误状态码。

        Args:
            status_code: HTTP状态码(如404, 500等)
            message: 错误消息内容
            elapsed_ms: 响应时间(毫秒)

        Returns:
            MagicMock: 模拟的错误Response对象
        """
        response = MagicMock(spec=requests.Response)
        response.status_code = status_code
        response.content = message.encode('utf-8')
        response.elapsed = timedelta(milliseconds=elapsed_ms)
        response.headers = {'Content-Type': 'text/plain'}
        response.text = message
        response.ok = False

        # 创建HTTPError异常
        error_msg = f'{status_code} Server Error: message'
        response.raise_for_status = MagicMock(
            side_effect=requests.exceptions.HTTPError(error_msg)
        )
        return response

    @staticmethod
    def redirect(location: str = 'https://github.com/new-url') -> MagicMock:
        """创建重定向响应(301/302)

        用于模拟重定向场景。

        Args:
            location: 重定向目标URL

        Returns:
            MagicMock: 模拟的重定向Response对象
        """
        response = MagicMock(spec=requests.Response)
        response.status_code = 301
        response.content = b'Redirect'
        response.elapsed = timedelta(milliseconds=30)
        response.headers = {'Location': location}
        response.url = location
        response.history = []
        return response

    @staticmethod
    def connection_error() -> MagicMock:
        """创建连接错误响应

        用于模拟网络连接失败场景。

        Returns:
            MagicMock: 模拟的连接错误Response对象
        """
        response = MagicMock(spec=requests.Response)
        response.status_code = 0
        response.elapsed = timedelta(milliseconds=10)
        response.content = b''
        response.headers = {}
        response.raise_for_status = MagicMock(
            side_effect=requests.exceptions.ConnectionError('Failed to establish connection')
        )
        return response

    @staticmethod
    def timeout_exception() -> MagicMock:
        """创建超时异常响应

        用于模拟抛出Timeout异常的场景。

        Returns:
            MagicMock: 模拟的超时异常Response对象
        """
        response = MagicMock(spec=requests.Response)
        response.status_code = 0
        response.elapsed = timedelta(seconds=30)
        response.content = b''
        response.headers = {}
        response.raise_for_status = MagicMock(
            side_effect=requests.exceptions.Timeout('Connection timed out')
        )
        return response

    @staticmethod
    def too_many_redirects() -> MagicMock:
        """创建重定向过多响应

        用于模拟重定向次数过多场景。

        Returns:
            MagicMock: 模拟的重定向过多Response对象
        """
        response = MagicMock(spec=requests.Response)
        response.status_code = 0
        response.elapsed = timedelta(milliseconds=100)
        response.content = b''
        response.headers = {}
        response.raise_for_status = MagicMock(
            side_effect=requests.exceptions.TooManyRedirects('Exceeded 30 redirects.')
        )
        return response

    @staticmethod
    def ssl_error() -> MagicMock:
        """创建SSL错误响应

        用于模拟SSL证书验证失败场景。

        Returns:
            MagicMock: 模拟的SSL错误Response对象
        """
        response = MagicMock(spec=requests.Response)
        response.status_code = 0
        response.elapsed = timedelta(milliseconds=50)
        response.content = b''
        response.headers = {}
        response.raise_for_status = MagicMock(
            side_effect=requests.exceptions.SSLError('SSL certificate verify failed')
        )
        return response


class TimeFactory:
    """时间值工厂类

    用于创建各种测试场景所需的时间值。
    """

    @staticmethod
    def standard() -> list:
        """创建标准时间序列

        包含正常网络请求的响应时间。

        Returns:
            list: timedelta对象列表
        """
        return [
            timedelta(milliseconds=50),
            timedelta(milliseconds=120),
            timedelta(milliseconds=80),
            timedelta(milliseconds=200),
            timedelta(milliseconds=150)
        ]

    @staticmethod
    def fast() -> list:
        """创建快速响应时间序列

        用于模拟高性能服务器。

        Returns:
            list: timedelta对象列表
        """
        return [
            timedelta(milliseconds=10),
            timedelta(milliseconds=15),
            timedelta(milliseconds=20)
        ]

    @staticmethod
    def slow() -> list:
        """创建慢速响应时间序列

        用于模拟高负载服务器或网络延迟。

        Returns:
            list: timedelta对象列表
        """
        return [
            timedelta(milliseconds=500),
            timedelta(milliseconds=800),
            timedelta(milliseconds=1200),
            timedelta(milliseconds=600)
        ]

    @staticmethod
    def timeout_threshold() -> timedelta:
        """获取默认超时阈值

        Returns:
            timedelta: 超时时间对象(30秒)
        """
        return timedelta(seconds=30)

    @staticmethod
    def warning_threshold() -> timedelta:
        """获取警告阈值

        超过此时间的响应将触发警告。

        Returns:
            timedelta: 警告时间对象(200毫秒)
        """
        return timedelta(milliseconds=200)


class RequestMockFactory:
    """请求模拟工厂类

    用于创建完整的请求模拟对象。
    """

    @staticmethod
    def create_get_request(
        url: str = 'https://github.com/user/repo',
        status_code: int = 200,
        elapsed_ms: int = 100,
        content: bytes = b'Repository found'
    ) -> MagicMock:
        """创建模拟的GET请求

        Args:
            url: 请求URL
            status_code: HTTP状态码
            elapsed_ms: 响应时间
            content: 响应内容

        Returns:
            MagicMock: 模拟的请求对象
        """
        mock_request = MagicMock()
        mock_request.url = url
        mock_request.method = 'GET'
        mock_request.headers = {}
        mock_request.kwargs = {}
        mock_request.elapsed = timedelta(milliseconds=elapsed_ms)

        # 创建响应对象
        mock_response = MagicMock()
        mock_response.status_code = status_code
        mock_response.content = content
        mock_response.headers = {'Content-Type': 'text/html'}
        mock_response.text = content.decode('utf-8')
        mock_response.ok = status_code < 400
        mock_response.elapsed = timedelta(milliseconds=elapsed_ms)
        mock_response.raise_for_status = MagicMock(return_value=None)

        mock_request.return_value = mock_response
        return mock_request

    @staticmethod
    def create_error_request(
        url: str = 'https://github.com/user/repo',
        status_code: int = 404
    ) -> MagicMock:
        """创建模拟的错误请求

        Args:
            url: 请求URL
            status_code: HTTP状态码

        Returns:
            MagicMock: 模拟的错误请求对象
        """
        mock_request = MagicMock()
        mock_request.url = url
        mock_request.method = 'GET'
        mock_request.headers = {}
        mock_request.kwargs = {}

        error_msg = f'{status_code} Not Found'
        mock_request.return_value = ResponseFactory.error(status_code, error_msg)
        return mock_request


# 便捷函数
def create_success_response(content: bytes = b'Success') -> MagicMock:
    """创建成功响应的便捷函数

    Args:
        content: 响应内容

    Returns:
        MagicMock: 模拟的成功响应对象
    """
    return ResponseFactory.success(content)


def create_timeout_response() -> MagicMock:
    """创建超时响应的便捷函数

    Returns:
        MagicMock: 模拟的超时响应对象
    """
    return ResponseFactory.timeout()


def create_error_response(status_code: int = 500) -> MagicMock:
    """创建错误响应的便捷函数

    Args:
        status_code: HTTP状态码

    Returns:
        MagicMock: 模拟的错误响应对象
    """
    return ResponseFactory.error(status_code)
