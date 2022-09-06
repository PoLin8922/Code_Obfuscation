#!/usr/bin/env python2
import os # os.walk
import fnmatch # to match a pattern
import subprocess

# input
rosdebian_dir = "~/rosdebian_files"
# output
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







# The directory for *.deb
rosdebian_dir = os.path.expanduser(rosdebian_dir)
rosdebian_dir = os.path.expandvars(rosdebian_dir)
#
record_installation_file_path = rosdebian_dir + '/'+ record_installation_file_name
# if os.path.exists(record_installation_file_path):
#     print("remove %s" % record_installation_file_path)
#     # Remove the package, entirely
#     _cmd = "rm %s" % record_installation_file_path
#     subprocess.call(_cmd, shell=True)

# Cleanup the file
with open(record_installation_file_path, "w") as _fh:
    _fh.write('')


print("-"*100)
print("\nPackages in %s:" % rosdebian_dir)

deb_pkg_path_list = find_deb_files(rosdebian_dir)

for _i, _path in enumerate(deb_pkg_path_list):
    _file_name = os.path.basename(_path)
    _idx_dot = _file_name.rfind('.deb')
    _module_name = _file_name[:_idx_dot]
    _idx_version = _file_name.find('_')
    if _idx_version > 0:
        _module_name = _module_name[:_idx_version]
    print("%d:\t%s" % (_i, _module_name))
    # Record the module name that are to be installed
    with open(record_installation_file_path, "a") as _fh:
        _fh.write( _module_name + '\n' )
    # Install the dpkg module
    # _cmd = "dpkg -i %s" % _file_name
    # subprocess.call(_cmd, shell=True, cwd=rosdebian_dir)
    _cmd = 'echo "%s"|sudo -S dpkg -i %s' % (pw, _path)
    subprocess.call(_cmd, shell=True)
