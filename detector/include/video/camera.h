#pragma once
#include <string>

// Structure to store camera information
struct Camera
{
    std::string id;
    std::string ip;
    std::string password;

    // Constructor
    Camera(const std::string &cameraId, const std::string &cameraIp, const std::string &cameraPassword)
        : id(cameraId), ip(cameraIp), password(cameraPassword) {}
};
