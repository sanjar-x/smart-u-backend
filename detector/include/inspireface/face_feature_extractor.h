#pragma once
#include <vector>
#include <string>
#include <opencv2/opencv.hpp>
#include "inspireface/session_manager.h"
#include "index/index_manager.h"
#include "messages/zmqbroker.h"
class FaceFeatureExtractor
{
public:
    FaceFeatureExtractor();
    ~FaceFeatureExtractor();

    std::pair<std::vector<std::string>, std::vector<HFFaceFeature>> extractImagesFeatures(
        const std::pair<std::vector<std::string>, std::vector<cv::Mat>> &images);

    HFFaceFeature extractFeature(const cv::Mat &image);
    void extractAndProcessFeatures(const cv::Mat &image, const std::string &cameraId, IndexManager &indexManager, Broker *broker);

private:
    HFSession session_;
    SessionManager sessionManager_;
};
