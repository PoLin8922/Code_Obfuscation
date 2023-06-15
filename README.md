# Code_Obfuscation

## Pre-request
- Install bloom_generate
```
// install for ros 18.04 noetic
sudo apt-get install python-bloom fakeroot

// install for ros 20.04 noetic
sudo apt-get install python3-bloom fakeroot
sudo apt-get install debhelper
```
- Install pyminifier
```
// install for ros 18.04 noetic
pip2 install pyminifier

// install for ros 20.04 noetic
pip3 install pyminifier
```
- Install package **Package_Packing** in repo_path (same directory as src)
    - make pyobfuscate executable
        ```
        // in Package_Packing
        $ chmod +x chmod +x pyobfuscate
        ```
- **Ensure that all required programs are installed in Makefiles**

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
$ bloom-generate rosdebian 
$　fakeroot debian/rules binary
```
### If a package that include self-define package
1. in ~/.ros/rosdep.yaml add self-define package
    ```
    # example:
    test-msgs:
      ubuntu: [ros-kinetic-test-msgs]
    ```
2. create /etc/ros/rosdep/sources.list.d/50-my-default.list 
    ```
    # contents：
    yaml file:///home/ubuntu/.ros/rosdep.yaml
    ```
3. rosdep update
4. packing it again
---
### Flowchart
![](https://hackmd.io/_uploads/HycwolmBh.png)

## Installing
- program : install.py
1. install .deb file
```
// in .deb file path
＄　sudo dpkg -i <.deb>
```
---
## Makefile format
- Header
```
cmake_minimum_required(VERSION 3.0.2)
project(<package_name>)
```

- Find catkin macros and libraries
```
find_package(catkin REQUIRED)
# if have DEPENDS
find_package(catkin REQUIRED COMPONENTS
  gazebo_ros
  rospy
)
```

- The catkin_package macro generates cmake config files for your package
```
catkin_package()
# if have DEPENDS
catkin_package(
 CATKIN_DEPENDS rospy std_msgs
)

include_directories(
  ${catkin_INCLUDE_DIRS}
)
```

- Install c librarys
```
add_library(recorder src/bag_recorder.cpp src/read_file.cpp)
target_link_libraries(recorder ${catkin_LIBRARIES} ${Boost_LIBRARIES})
install(TARGETS recorder
  ARCHIVE DESTINATION ${CATKIN_PACKAGE_LIB_DESTINATION}
  LIBRARY DESTINATION ${CATKIN_PACKAGE_LIB_DESTINATION})
```

- Install c programs
```
add_executable(3D_map_loader nodes/3D_map_loader.cpp)
target_link_libraries(3D_map_loader ${catkin_LIBRARIES} ${PCL_LIBRARIES})
install(TARGETS 3D_map_loader
  RUNTIME DESTINATION ${CATKIN_PACKAGE_BIN_DESTINATION})
```

- Install python
```
catkin_install_python(PROGRAMS
  scripts/mapping_gui.py
  DESTINATION ${CATKIN_PACKAGE_BIN_DESTINATION}
)
```

- Install files
```
install(FILES
  rviz/rviz.rviz
  DESTINATION ${CATKIN_PACKAGE_SHARE_DESTINATION}/rviz
)
```

- Install directory 
```
install(DIRECTORY
  launch
  maps
  DESTINATION ${CATKIN_PACKAGE_SHARE_DESTINATION}
)
```

- Destination explanation : 
    - ${CATKIN_PACKAGE_BIN_DESTINATION} : install in /opt/ros/melodic/lib
        - c and python program file
    - ${CATKIN_PACKAGE_SHARE_DESTINATION} : install in /opt/ros/melodic/share
        - launch yaml... txt file
    - ${CATKIN_PACKAGE_INCLUDE_DESTINATION : install in /opt/ros/melodic/include
        - .h file

- Other installation ：
    - https://blog.csdn.net/m0_60346726/article/details/129754237?ops_request_misc=%257B%2522request%255Fid%2522%253A%2522168420515116800182116700%2522%252C%2522scm%2522%253A%252220140713.130102334.pc%255Fall.%2522%257D&request_id=168420515116800182116700&biz_id=0&utm_medium=distribute.pc_search_result.none-task-blog-2
---
## Common Makefile mistakes
1. CMakeLists中Package名稱不能大寫
2. CMakeLists中find_package()需在catkin_package()上面
3. CMakeLists中無catkin_package()，雖然dpkg成功，但環境中仍會無該package
4. CMakeLists中皆需是相對路徑，不能放絕對路徑
5. 若install後的package某些功能無法正常執行，檢查CMakeList中是否有重要程式或檔案沒有被install

