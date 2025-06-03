import os, sys

#절대 경로 반환
def get_resource_path(*relative_parts):
    base = os.path.dirname(os.path.abspath(sys.argv[0]))  # 실행파일 위치 기준
    return os.path.join(base, *relative_parts)
