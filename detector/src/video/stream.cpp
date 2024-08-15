#include "video/stream.h"

Stream::Stream(const Camera &camera, const std::string &pipeline)
    : camera(camera), capture(pipeline, cv::CAP_GSTREAMER)
{
    if (!capture.isOpened())
    {
        std::cerr << "Failed to open video stream for camera: " << camera.id << std::endl;
    }
}

bool Stream::isOpen() const
{
    return capture.isOpened();
}
