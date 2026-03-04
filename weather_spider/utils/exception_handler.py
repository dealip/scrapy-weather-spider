import functools
from weather_spider.utils.logger_helper import get_default_logger


def handle_exceptions(logger_name="default", re_raise=True, default_return=None):
    """
    通用异常处理装饰器
    :param logger_name: 日志器名称
    :param re_raise: 是否重新抛出异常（Scrapy 中大部分场景需要 True）
    :param default_return: 异常时的默认返回值（re_raise=False 时生效）
    """

    def decorator(func):
        @functools.wraps(func)  # 保留原函数的元信息（关键）
        def wrapper(*args, **kwargs):
            logger = get_default_logger(logger_name)
            try:
                return func(*args, **kwargs)
            except Exception as e:
                # 记录详细的异常信息：函数名 + 入参 + 异常内容
                logger.error(
                    f"函数 {func.__name__} 执行失败 | 参数: args={args}, kwargs={kwargs} | 异常: {str(e)}",
                    exc_info=True,  # 打印完整的堆栈信息（排查问题必备）
                )
                if re_raise:
                    raise  # 重新抛出，让上层逻辑处理（比如 Scrapy 忽略该请求）
                return default_return

        return wrapper

    return decorator
