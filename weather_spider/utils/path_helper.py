import os
import sys

# 立即执行：将当前文件所在目录的父目录添加到路径
_current_file = os.path.abspath(__file__)
# utils目录的父目录是 weather_spider，再父目录是 weather_spider，再父目录才是项目根目录
_project_root = os.path.dirname(os.path.dirname(os.path.dirname(_current_file)))
if _project_root not in sys.path:
    sys.path.insert(0, _project_root)


def get_project_root() -> str:
    """
    获取项目根目录
    :return: 项目根目录绝对路径
    """
    # 当前文件（path_helper.py)的绝对路径
    current_file_path = os.path.abspath(__file__)
    # 向上找三级：utils/ → weather_spider/ → weather_spider/ → 项目根目录
    project_root = os.path.dirname(os.path.dirname(os.path.dirname(current_file_path)))
    if not os.path.exists(project_root):
        raise FileNotFoundError(f"项目根目录不存在！{project_root}")
    return project_root


def add_project_path() -> None:
    """
    将项目核心目录加入Python搜索路径
    """
    project_core_dir = get_project_root()
    if project_core_dir not in sys.path:
        sys.path.append(project_core_dir)


def get_project_path(sub_dir: str = None, filename: str = None) -> str:
    """
    拼接项目根目录下的文件路径
    :param sub_dir: 项目根目录下的子目录名（可选）
    :param filename: 文件名（可选）
    :return: 文件绝对路径
    """
    project_root = get_project_root()
    # 如果没有指定子目录和文件名，直接返回项目根目录
    if sub_dir is None and filename is None:
        return get_project_root()

    # 处理子目录
    path_parts = [project_root]
    if sub_dir is not None:
        sub_dir_segments = sub_dir.strip(os.sep).split(os.sep)
        path_parts.extend(sub_dir_segments)
    if filename is not None:
        filename_segments = filename.strip(os.sep).split(os.sep)
        path_parts.extend(filename_segments)
    # 拼接路径
    result_path = os.path.join(*path_parts)

    # 如果指定了文件名，创建父目录；否则创建整个目录
    if filename:
        parent_dir = os.path.dirname(result_path)
        if not os.path.exists(parent_dir):
            os.makedirs(parent_dir, exist_ok=True)
    elif sub_dir and not os.path.exists(result_path):
        os.makedirs(result_path, exist_ok=True)
    return result_path


def get_data_path(sub_dir: str, filename: str) -> str:
    """
    拼接data目录下的文件路径
    """
    return get_project_path(os.path.join("data", sub_dir), filename)


# 执行添加项目路径
add_project_path()
