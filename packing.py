#!/usr/bin/env python2
import os # os.walk
import fnmatch # to match a pattern
import subprocess

# input
file_path = os.path.abspath(__file__)
repo_path = file_path.replace("/Package_Packing/packing.py", "")
deployment_scripts_path = file_path.replace("/packing.py", "")
# output
rosdebian_dir = "~/rosdebian_files"

'''
# White list
#------------------------------------------------------#
# pkg_white_list = ['agv','docking_navigation_2','multirobot_nav','escape_recovery_2']
pkg_white_list = None

# Black list
#------------------------------------------------------#
pkg_black_list = None

# Delete-anyway list
#------------------------------------------------------#
# pkg_delete_list = [ 'map_server', 'simple_layers','apriltags_ros','apriltags',
#                     'tag_mapping','docking_navigation','amcl_aux_localization','msg_recorder',
#                     'detection_viz','drivenet','camera_utils','object_costmap_generator','drivenet_lib'
#                     ]
pkg_delete_list = None
'''

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

def find_packages(path):
    pattern = 'package.xml'
    path_list = find(pattern, path)
    _pkg_path_list = []
    for _path in path_list:
        _dir_path = os.path.dirname(_path)
        _pkg_path_list.append(_dir_path)
    return _pkg_path_list

def find_python_packages(path):
    pattern = 'package.xml'
    path_list = find(pattern, path)
    # Check existance of python file
    _pkg_path_list = []
    for _path in path_list:
        _dir_path = os.path.dirname(_path)
        # print(_dir_path)
        _py_list = find("*.py", _dir_path)
        if len(_py_list) > 0:
            _pkg_path_list.append(_dir_path)
    return _pkg_path_list


def find_python_files_in_a_packag(pkg_path):
    # print(_dir_path)
    _py_list = find("*.py", pkg_path)
    return _py_list



def minify_python_script(py_file_path):
    _tmp_file_name = "tmp.py"
    _cmd = "./pyobfuscate %s > %s" % (py_file_path, _tmp_file_name)
    subprocess.call(_cmd, shell=True, cwd=os.path.dirname(deployment_scripts_path + "/pyobfuscate"))
    _cmd = "mv %s %s" % (_tmp_file_name, py_file_path) 
    subprocess.call(_cmd, shell=True, cwd=os.path.dirname(deployment_scripts_path + '/' + _tmp_file_name))
    _cmd = "pyminifier --nominify --gzip %s > %s" % (py_file_path, _tmp_file_name)
    subprocess.call(_cmd, shell=True, cwd=os.path.dirname(py_file_path))
    _cmd = "mv %s %s" % (_tmp_file_name, py_file_path) 
    subprocess.call(_cmd, shell=True, cwd=os.path.dirname(py_file_path)) 
    # _cmd = "python2 -m py_compile %s" % (py_file_path) 
    # subprocess.call(_cmd, shell=True, cwd=os.path.dirname(py_file_path)) 
    # _cmd = "mv %s %s" % (py_file_path + 'c', py_file_path) 
    # subprocess.call(_cmd, shell=True, cwd=os.path.dirname(py_file_path))
    _cmd = "chmod u+x %s" % py_file_path
    subprocess.call(_cmd, shell=True)


#---------------------------------------------------------------------#
# Make the directory for *.deb
rosdebian_dir = os.path.expanduser(rosdebian_dir)
rosdebian_dir = os.path.expandvars(rosdebian_dir)
try:
    # _out = subprocess.check_output(["mkdir", "-p", rosdebian_dir], stderr=subprocess.STDOUT)
    os.makedirs(rosdebian_dir)
    print("The directory <%s> has been created." % rosdebian_dir)
except:
    print("The directry <%s> already exists." % rosdebian_dir)
    pass


# Fins packages
print("-"*100)
print("\nPackages in repo. [%s]:" % repo_path)
pkg_path_list = find_packages(repo_path)
# print(python_pkg_path_list)
for _i, _path in enumerate(pkg_path_list):
    print("%d:\t%s" % (_i, _path))


print("-"*100)
print("\nPackages that include python scripts:")
python_pkg_path_list = find_python_packages(repo_path)
# print(python_pkg_path_list)
for _i, _path in enumerate(python_pkg_path_list):
    print("%d:\t%s" % (_i, _path))
print("-"*100)


def rm_directory(_path):
    # Remove the package, entirely
    _cmd = "rm -rf %s" % _path
    subprocess.call(_cmd, shell=True)
    _pkg_name = os.path.basename(_path)
    print("---[%s] removed" % _pkg_name)


# Generating rosdebians

for _i, _path in enumerate(pkg_path_list):
    _pkg_name = os.path.basename(_path)
    
    '''
    # Filtering
    #----------------------------------------------------------------#
    _skip_build = False
    # Whitelist
    if (pkg_white_list is not None) and not (_pkg_name in pkg_white_list):
        _skip_build = True
    # Blacklist
    if (pkg_black_list is not None) and (_pkg_name in pkg_black_list):
        _skip_build = True
    # Delete anyway
    if (pkg_delete_list is not None) and (_pkg_name in pkg_delete_list):
        # delete anyway
        # rm_directory(_path)
        _skip_build = True
    #----------------------------------------------------------------#
    # _skip_build
    if _skip_build:
        continue
    #----------------------------------------------------------------#
    print("\n")
    print("-"*30)
    print("%d:\t%s" % (_i, _pkg_name))
    '''

    # Processing python files
    if _path in python_pkg_path_list:
        print("\n************** Found python files, minify it **************\n")
        _py_list = find_python_files_in_a_packag(_path)
        for _i, _py_path in enumerate(_py_list):
            print("%d:\t%s" % (_i, _py_path))
            minify_python_script(_py_path)

    # pack debian
    subprocess.call("bloom-generate rosdebian", shell=True, cwd=_path)
    # make
    subprocess.call("fakeroot debian/rules binary", shell=True, cwd=_path)
    # collect the *.deb to rosdebian_dir
    _cmd = "mv %s %s" % ("*.deb", rosdebian_dir+'/')
    subprocess.call(_cmd, shell=True, cwd=os.path.dirname(_path))
    _cmd = "mv %s %s" % ("*.ddeb", rosdebian_dir+'/') # *.ddeb files
    subprocess.call(_cmd, shell=True, cwd=os.path.dirname(_path))
    print("---[%s] added to %s" % (_pkg_name, rosdebian_dir+'/'))
    # Remove the package, entirely
    # rm_directory(_path)


# Copy the installation and uninstallation task_scripts
_cmd = "cp %s %s" % (deployment_scripts_path+'/install.py', rosdebian_dir+'/')
subprocess.call(_cmd, shell=True)
_cmd = "cp %s %s" % (deployment_scripts_path+'/uninstall.py', rosdebian_dir+'/')
subprocess.call(_cmd, shell=True)

# check
pkg_path_list = find_packages(repo_path)
pkg_success_list = []
pkg_fail_list = []
for _i, _path in enumerate(pkg_path_list):
    _pkg_name = os.path.basename(_path)
    pkg_fail_list.append(_pkg_name)
    if(_path.find("debian") != -1):
        pkg_fail_list.remove(_pkg_name)
        pkg_fail_list.remove(_pkg_name)
        pkg_success_list.append(_pkg_name) 

print("\n************** Success package list **************\n")
print(pkg_success_list)
print("\n************** Fial package list **************\n")
print(pkg_fail_list)