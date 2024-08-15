#pragma once
#include <string>
#include <opencv2/opencv.hpp>
#include "video/camera.h"

struct Stream
{
    Camera camera;
    cv::VideoCapture capture;

    Stream(const Camera &camera, const std::string &pipeline);

    bool isOpen() const;
};