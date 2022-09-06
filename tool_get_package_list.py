#!/usr/bin/env python2
import os # os.walk
import fnmatch # to match a pattern

# os.walk is the answer, this will find the first match:
def find(name, path):
    for root, dirs, files in os.walk(path):
        if name in files:
            return os.path.join(root, name)

# And this will find all matches:
def find_all(name, path):
    path_list = []
    for root, dirs, files in os.walk(path):
        if name in files:
            path_list.append(os.path.join(root, name))
    return path_list

# And this will match a pattern:
def find(pattern, path):
    path = os.path.expanduser(path)
    path = os.path.expandvars(path)
    path_list = []
    for root, dirs, files in os.walk(path):
        for name in files:
            if fnmatch.fnmatch(name, pattern):
                path_list.append(os.path.join(root, name))
    return path_list

def find_python_packages(path):
    pattern = 'package.xml'
    path = os.path.expanduser(path)
    path = os.path.expandvars(path)
    path_list = []
    for root, dirs, files in os.walk(path):
        for name in files:
            if fnmatch.fnmatch(name, pattern):
                path_list.append(os.path.join(root, name))
    # Check existance of python file
    _pkg_path_list = []
    for _path in path_list:
        _dir_path = os.path.dirname(_path)
        # print(_dir_path)
        _py_list = find("*.py", _dir_path)
        if len(_py_list) > 0:
            _pkg_path_list.append(_dir_path)
    return _pkg_path_list


print("-"*100)
print("\nPackages in kenmec_agv repo.:")

path_list = find('package.*', '~/agv_ws/src/kenmec_agv')
# print(path_list)
for _i, _path in enumerate(path_list):
    # print("%d:\t%s" % (_i, _path))
    # _base = os.path.basename(_path)
    _dir = os.path.dirname(_path)
    # _pkg = os.path.basename(os.path.dirname(_path))
    # print(_pkg)
    print("%d:\t%s" % (_i, _dir))
    # print("%d:\t%s" % (_i, _pkg))
    # print("%d: %s\t%s" % (_i, _pkg, _dir))
print("-"*100)

print("\nPackages that include python scripts:")

python_pkg_path_list = find_python_packages('~/agv_ws/src/kenmec_agv')
# print(python_pkg_path_list)
for _i, _path in enumerate(python_pkg_path_list):
    print("%d:\t%s" % (_i, _path))
print("-"*100)
