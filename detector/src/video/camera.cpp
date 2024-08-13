// std::string gst_pipeline = "rtspsrc location=rtsp://admin:" + camera.password + "@" + camera.ip_address + ":554/Streaming/Channels/101 protocols=tcp timeout=50 latency=0 ! rtph265depay ! h265parse ! nvh265dec ! videoconvert ! appsink max-buffers=1 drop=true sync=false";

// camera.capture.open(gst_pipeline, cv::CAP_GSTREAMER);
// if (!camera.capture.isOpened())
// {
//     Logger::getInstance().log(Logger::ERROR, "Failed to open video capture for camera with IP: " + camera.ip_address);
// }
