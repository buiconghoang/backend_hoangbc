# from filemonitor.config import config
from filemonitor import constant
import os

def make_hash(file_path, size, date_updated):
    str_builder = file_path + str(size) + str(date_updated) + str(constant.SECRET_HASH_KEY)
    return hash(str_builder)

def get_file_childs_path(root_path):
    rv = []
    if os.path.isfile(root_path):
        rv.append(os.path.abspath(root_path))
    if os.path.isdir(root_path):
        for root, dirs, files in os.walk(root_path, topdown=False):
            for name in files:
                rv.append(os.path.abspath(os.path.join(root, name)))
    return rv
    