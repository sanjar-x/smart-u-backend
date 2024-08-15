cmake_minimum_required(VERSION 3.10)
project(main)

set(CMAKE_CXX_STANDARD 17)
set(CMAKE_CXX_STANDARD_REQUIRED True)

# Указание путей к заголовочным файлам
include_directories(
    /usr/local/include
    ${PROJECT_SOURCE_DIR}/include
    ${PROJECT_SOURCE_DIR}/include/database
    ${PROJECT_SOURCE_DIR}/include/index
    ${PROJECT_SOURCE_DIR}/include/inspireface
    ${PROJECT_SOURCE_DIR}/include/messages
    ${PROJECT_SOURCE_DIR}/include/utils
    ${PROJECT_SOURCE_DIR}/include/video

)

link_directories(/usr/local/lib)

set(SOURCES
    src/database/camera_repository.cpp
    src/database/database.cpp
    src/database/image_repository.cpp
    src/index/index_manager.cpp
    src/inspirefase/face_feature_extractor.cpp
    src/inspirefase/session_manager.cpp
    src/messages/zmqbroker.cpp
    src/utils/common.cpp
    src/utils/logger.cpp 
    src/video/camera.cpp
    src/video/stream.cpp
    src/video/streamer.cpp
    main.cpp
)

set(OpenCV_DIR "/usr/local/lib/cmake/opencv4")

find_package(OpenCV REQUIRED core imgproc highgui imgcodecs videoio)
find_package(PkgConfig REQUIRED)
pkg_check_modules(PQXX REQUIRED libpqxx)
pkg_check_modules(ZeroMQ REQUIRED libzmq)
find_package(Faiss REQUIRED)

add_executable(main ${SOURCES})

target_link_libraries(main PRIVATE ${OpenCV_LIBS} ${ZeroMQ_LIBRARIES} ${PQXX_LIBRARIES} /usr/local/lib/libfaiss.so InspireFace)

