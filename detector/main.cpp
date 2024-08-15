#include <iostream>
#include <thread>
#include "utils/logger.h"
#include "database/image_repository.h"
#include "database/camera_repository.h"
#include "inspireface/face_feature_extractor.h"
#include "index/index_manager.h"
#include "messages/zmqbroker.h"
#include "video/camera.h"
#include "video/streamer.h"

int main()
{
    std::cout << "Starting the program..." << std::endl;

    std::cout << "Launching InspireFace..." << std::endl;
    HResult result = HFLaunchInspireFace("/home/ocean/Desktop/smart-u-backend/detector/resource/archive/Megatron");
    if (result != HSUCCEED)
    {
        std::cerr << "Failed to launch InspireFace. Error code: " << result << std::endl;
        return 1;
    }

    IndexManager indexManager;
    std::cout << "Building the index..." << std::endl;
    indexManager.buildIndex();

    CameraRepository cameraRepository;
    std::cout << "Fetching cameras from the database..." << std::endl;
    std::vector<Camera> cameras = cameraRepository.fetchCameras();
    std::cout << "Cameras fetched: " << cameras.size() << std::endl;

    if (cameras.empty())
    {
        std::cerr << "No cameras were fetched from the database. Exiting." << std::endl;
        return 1;
    }

    std::string brokerEndpoint = "ipc:///tmp/zeromq-ipc";
    Streamer streamer(cameras, indexManager, brokerEndpoint);

    streamer.processStreams();

    std::cout << "Program finished." << std::endl;

    return 0;
}
