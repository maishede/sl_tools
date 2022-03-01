import shutil
import os
import datetime
import configparser

config_path = "./config.ini"
bak_dir_name = "bak"


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


def save():
    # 从源文件拷出到目标文件夹,同时备份一份到备份文件夹
    config = read_config()
    source_path = config.get("config", "source_path")
    save_path = config.get("config", "save_path")
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
    files = find_sl_files(save_path)
    for file in files:
        copy_file(file, source_path)
