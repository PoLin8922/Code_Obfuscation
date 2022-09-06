#!/usr/bin/env python2
import os # os.walk
import fnmatch # to match a pattern
import subprocess

# input
rosdebian_dir = "~/rosdebian_files"
record_installation_file_name = "installed_modules.txt"

# print('NOTE: please use "sudo" for executing this script.')
try:
    txt_input = raw_input
except NameError:
    txt_input = input
pw = txt_input("Please enter the password of this user: ")

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

def find_deb_files(path):
    pattern = '*.deb'
    path_list = find(pattern, path)
    return path_list






#---------------------------------------------------------------------#
# The directory for *.deb
rosdebian_dir = os.path.expanduser(rosdebian_dir)
rosdebian_dir = os.path.expandvars(rosdebian_dir)
#
record_installation_file_path = rosdebian_dir + '/'+ record_installation_file_name

# Read installed modules
_line_list = []
with open(record_installation_file_path, "r") as _fh:
    _line_list = _fh.readlines()
# Remove new line charactors
_module_name_list = []
for _line in _line_list:
    _module_name_list.append(_line.strip())
print(_module_name_list)



print("-"*100)
print("\nPackages installed:")

for _i, _module_name in enumerate(_module_name_list):
    print("%d:\t%s" % (_i, _module_name))
    _cmd = 'echo "%s"|sudo -S apt-get remove %s -y' % (pw, _module_name)
    subprocess.call(_cmd, shell=True)
