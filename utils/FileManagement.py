import yaml
import os

def read_conf(filename='config.yaml'):
    # 自动拼接 config.yaml 的绝对路径
    base_path = os.path.abspath(os.path.dirname(__file__))  # 当前 utils 文件夹
    config_path = os.path.join(base_path, '..', filename)   # 回到项目根目录找 config.yaml

    with open(config_path, 'r', encoding='utf-8') as f:
        return yaml.safe_load(f)
