cmake_minimum_required(VERSION 3.10)
project(detector)

set(CMAKE_CXX_STANDARD 17)
set(CMAKE_CXX_STANDARD_REQUIRED True)
set(CMAKE_PREFIX_PATH "/usr/lib/x86_64-linux-gnu/pkgconfig")

include_directories(
    ${PROJECT_SOURCE_DIR}/include
    ${PROJECT_SOURCE_DIR}/include/database
    ${PROJECT_SOURCE_DIR}/include/index
    ${PROJECT_SOURCE_DIR}/include/inspireface
    ${PROJECT_SOURCE_DIR}/include/messages
    ${PROJECT_SOURCE_DIR}/include/utils
    ${PROJECT_SOURCE_DIR}/include/video
)

set(SOURCES
    src/database/camera_repository.cpp
    src/database/database.cpp
    src/database/image_repository.cpp
    src/detector.cpp
    src/index/faiss.cpp
    src/messages/zmqbroker.cpp
    src/recogination.cpp
    src/utils/common.cpp
    src/utils/logger.cpp 
    src/video/camera.cpp
    src/video/streamer.cpp
    main.cpp
)


find_package(OpenCV REQUIRED)

find_package(PkgConfig REQUIRED)
pkg_check_modules(ZeroMQ REQUIRED libzmq)
add_executable(detector ${SOURCES})
target_link_libraries(detector ${OpenCV_LIBS} ${ZeroMQ_LIBRARIES})
