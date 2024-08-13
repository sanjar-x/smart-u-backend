#pragma once

#include <string>
#include <opencv2/opencv.hpp>

struct Camera
{
    std::string id;
    std::string ip_address;
    std::string password;
    cv::VideoCapture capture;
};
