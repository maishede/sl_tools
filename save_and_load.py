import shutil
import os
import datetime
import configparser

config_path = "./config.ini"
bak_dir_name = "bak"
SOURCE_PATH_NAME = "自动存档"
SAVE_PATH_NAME = "手动存档"


def read_config():
    config = configparser.ConfigParser()
    config.read(config_path, encoding='utf8')
    return config


def copy_file(raw_file_path, tar_file_path):
    shutil.copy(raw_file_path, tar_file_path)


def find_sl_files(path):
    config = read_config()
    sl_suffix = config.get("config", "sl_suffix")
    sl_bak_suffix = config.get("config", "sl_bak_suffix")
    tar_list = []
    file_names = os.listdir(path)
    for file_name in file_names:
        file_path = os.path.join(path, file_name)
        if os.path.isfile(file_path) and (file_path.endswith(sl_suffix) or file_path.endswith(sl_bak_suffix)):
            tar_list.append(file_path)
    return tar_list


def save_file_bak():
    config = read_config()
    save_path = config.get("config", "save_path")
    bak_path = os.path.join(save_path, bak_dir_name)
    timestamp = datetime.datetime.now().strftime("%Y-%m-%d-%H-%M-%S-%f")
    timestamp_path = os.path.join(bak_path, timestamp)
    os.makedirs(timestamp_path)
    return timestamp_path


def create_config_file():
    with open(config_path, "w+") as f:
        f.close()
    config = configparser.ConfigParser()
    config.read(config_path, encoding='utf8')
    config.add_section("config")
    config.set("config", "source_path", "")
    config.set("config", "save_path", "")
    config.set("config", "sl_suffix", ".sl2")
    config.set("config", "sl_bak_suffix", ".sl2.bak")
    config.write(open(config_path, "r+", encoding='utf8'))


def init_config():
    if not os.path.exists(config_path):
        create_config_file()


def judge_config_path(source_path, save_path):
    if not source_path and not save_path:
        raise Exception(f"请配置{SOURCE_PATH_NAME}路径\n请配置{SAVE_PATH_NAME}路径")
    if not save_path and source_path:
        raise Exception(f"请配置{SAVE_PATH_NAME}路径")
    if not source_path and save_path:
        raise Exception(f"请配置{SOURCE_PATH_NAME}路径")

    source_exist = os.path.exists(source_path)
    save_exist = os.path.exists(save_path)

    if not source_exist and not save_exist:
        raise Exception(f"{SOURCE_PATH_NAME}路径错误,请重新配置:当前位置:{source_path}\n{SAVE_PATH_NAME}路径错误,请重新配置:当前位置:{save_path}")

    if not source_exist and save_exist:
        raise Exception(f"{SOURCE_PATH_NAME}路径错误,请重新配置:当前位置{source_path}")
    if not os.path.exists(save_path):
        raise Exception(f"{SAVE_PATH_NAME}路径错误,请重新配置:当前位置{save_path}")


def save():
    # 从源文件拷出到目标文件夹,同时备份一份到备份文件夹
    # TODO 是否限制备份文件数量,防止占用过多磁盘,没想好怎么设计这个规则
    config = read_config()
    source_path = config.get("config", "source_path")
    save_path = config.get("config", "save_path")
    judge_config_path(source_path, save_path)
    files = find_sl_files(source_path)
    bak_path = save_file_bak()
    for file in files:
        copy_file(file, save_path)
        copy_file(file, bak_path)


def load():
    config = read_config()
    source_path = config.get("config", "source_path")
    save_path = config.get("config", "save_path")
    # 从存档文件夹复制到源文件夹
    judge_config_path(source_path, save_path)
    files = find_sl_files(save_path)
    for file in files:
        copy_file(file, source_path)
