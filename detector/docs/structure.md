detector/
├── include/
│   ├── database/
│   │   ├── camera_repository.h
│   │   ├── database.h
│   │   └── image_repository.h
│   ├── index/
│   │   └── index_manager.h
│   ├── inspireface/
│   │   ├── face_feature_extractor.h
│   │   ├── herror.h
│   │   ├── inspireface.h
│   │   ├── intypedef.h
│   │   └── session_manager.h
│   ├── messages/
│   │   └── zmqbroker.h
│   ├── video/
│   │   ├── camera.h
│   │   └── streamer.h
│   └── utils/
│       ├── logger.h
│       └── common.h
├── src/
│   ├── database/
│   │   ├── camera_repository.cpp
│   │   ├── database.cpp
│   │   └── image_repository.cpp
│   ├── messages/
│   │   └── zmqbroker.cpp
│   ├── video/
│   │   ├── camera.cpp
│   │   └── streamer.cpp
│   ├── index/
│   │   └── index_manager.cpp
│   ├── inspireface/
│   │   ├── face_feature_extractor.cpp
│   │   └── session_manager.cpp
│   └── utils/
│       ├── loger.cpp
│       └── common.cpp
├── test/
│   ├── database/
│   │   └── test_database.cpp
│   ├── messages/
│   │   └── test_messagebroker.cpp
│   ├── video/
│   │   └── test_video.cpp
│   └── main_test.cpp
├── docs/
│   ├── architecture.md
│   ├── usage.md
│   └── api_reference.md
├── scripts/
│   ├── build.sh
│   ├── run.sh
│   └── clean.sh
├── cmake/
│   └── FindMyLibrary.cmake
├── CMakeLists.txt
├── main.cpp
└── README.md
