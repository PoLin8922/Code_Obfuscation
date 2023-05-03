# Code_Obfuscation

## Pre-request
- install bloom_generate
```
// install for ros 20.04 noetic
sudo apt-get install python3-bloom fakeroot
```
- install pyminifier
```
pip install pyminifier
```
- install package **Package_Packing** in repo_path (same directory as src)
```
// in Package_Packing
$ chmod +x chmod +x pyobfuscate
```
- **Ensure Makefiles have installed all required programs**

## Packing
- program : packing.py
1. obfuscate python file
    -  obfuscate
    ```
    $ ./pyobfuscate example.py > example_obf.py
    ```
    -  compress
    ```
    ＄　pyminifier --nominify --gzip example_obf.py > example_zip.py
    ```
    - make file executable
    ```
    $　chmod u+x example.py
    ```

2. packing package to .deb file
```
// in package directory
$ bloom-generate rosdebian --os-name ubuntu --ros-distro noetic
$　fakeroot debian/rules binary
```
---
## If a package that include self-define package
1. In ~/.ros/rosdep.yaml 新增 msg
    - example:
    ```
    test-msgs:
      ubuntu: [ros-kinetic-test-msgs]
    ```
2. 創建 /etc/ros/rosdep/sources.list.d/50-my-default.list 
    - 內容：
    ```
    yaml file:///home/ubuntu/.ros/rosdep.yaml
    ```
3. rosdep update
4. 再次壓縮 package
---
## Installing
- program : install.py
1. install .deb file
```
// in .deb file path
＄　sudo dpkg -i <.deb>
```

---
## Makefile format example
- install file : 
    - ${CATKIN_PACKAGE_BIN_DESTINATION} : install in /opt/ros/melodic/lib
        - c and python program file
    - ${CATKIN_PACKAGE_SHARE_DESTINATION} : install in /opt/ros/melodic/share
        - launch yaml... txt file
```
cmake_minimum_required(VERSION 3.0.2)
project(<package_name>)

## Find catkin macros and libraries
find_package(catkin REQUIRED)
# if have DEPENDS
find_package(catkin REQUIRED COMPONENTS
  gazebo_ros
  rospy
)

## The catkin_package macro generates cmake config files for your package
catkin_package()
# if have DEPENDS
catkin_package(
 CATKIN_DEPENDS rospy std_msgs
)

include_directories(
  ${catkin_INCLUDE_DIRS}
)

## c programs
add_executable(3D_map_loader nodes/3D_map_loader.cpp)
target_link_libraries(3D_map_loader ${catkin_LIBRARIES} ${PCL_LIBRARIES})
install(TARGETS 3D_map_loader
  RUNTIME DESTINATION ${CATKIN_PACKAGE_BIN_DESTINATION})
  
## python
catkin_install_python(PROGRAMS
  scripts/mapping_gui.py
  DESTINATION ${CATKIN_PACKAGE_BIN_DESTINATION}
)

## install files
install(FILES
  rviz/rviz.rviz
  DESTINATION ${CATKIN_PACKAGE_SHARE_DESTINATION}/rviz
)

# install directory 
install(
  DIRECTORY
    launch
  DESTINATION
      ${CATKIN_PACKAGE_SHARE_DESTINATION}
)
```

