from pathlib import Path
import sys
import os


def get_executable_path():
    if getattr(sys, "frozen", False):
        return Path(sys.executable).parent.as_posix()
    else:
        return Path.cwd().as_posix()


ROOT_DIR = get_executable_path()
TIMBRE_DIR_PATH = Path(ROOT_DIR + "/static/timbre")
TIMBRE_DIR_PATH.mkdir(parents=True, exist_ok=True)
TIMBRE_DIR = TIMBRE_DIR_PATH.as_posix()

LOGS_DIR_PATH = Path(ROOT_DIR + "/logs")
LOGS_DIR_PATH.mkdir(parents=True, exist_ok=True)
LOGS_DIR = LOGS_DIR_PATH.as_posix()

# 获取环境变量
WEB_ADDRESS = os.getenv("WEB_ADDRESS", "127.0.0.1:9966")

VERSION = "1.0.0"
NAME = "ChatTTS timbre"
