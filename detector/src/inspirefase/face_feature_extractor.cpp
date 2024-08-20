#include "inspireface/face_feature_extractor.h"
#include "index/index_manager.h"
#include "utils/logger.h"

FaceFeatureExtractor::FaceFeatureExtractor()
{
    Logger &logger = Logger::getInstance();

    session_ = sessionManager_.createSession();
    if (!session_)
    {
        logger.log(Logger::ERROR, "Failed to create session in FaceFeatureExtractor.");
    }
    else
    {
        logger.log(Logger::INFO, "Session created successfully in FaceFeatureExtractor.");
    }
}

FaceFeatureExtractor::~FaceFeatureExtractor()
{
    if (session_)
    {
        sessionManager_.releaseSession(session_);
        Logger::getInstance().log(Logger::INFO, "Session released in FaceFeatureExtractor destructor.");
    }
}

std::pair<std::vector<std::string>, std::vector<HFFaceFeature>> FaceFeatureExtractor::extractImagesFeatures(
    const std::pair<std::vector<std::string>, std::vector<cv::Mat>> &images)
{
    Logger &logger = Logger::getInstance();
    std::vector<std::string> ids;
    std::vector<HFFaceFeature> features;

    for (size_t i = 0; i < images.first.size(); ++i)
    {
        const std::string &id = images.first[i];
        const cv::Mat &image = images.second[i];

        HFFaceFeature feature = extractFeature(image);
        if (feature.size > 0)
        {
            ids.push_back(id);
            features.push_back(feature);
            logger.log(Logger::INFO, "Extracted features for image ID: " + id);
        }
        else
        {
            logger.log(Logger::ERROR, "Failed to extract features for image ID: " + id);
        }
    }

    return std::make_pair(ids, features);
}

HFFaceFeature FaceFeatureExtractor::extractFeature(const cv::Mat &image)
{
    Logger &logger = Logger::getInstance();
    HFFaceFeature faceFeature = {0};

    if (image.empty())
    {
        logger.log(Logger::ERROR, "Provided image is empty.");
        return faceFeature;
    }

    HFImageData imageData = {0};
    imageData.data = image.data;
    imageData.format = HF_STREAM_BGR;
    imageData.height = image.rows;
    imageData.width = image.cols;
    imageData.rotation = HF_CAMERA_ROTATION_0;

    HFImageStream stream;
    HResult result = HFCreateImageStream(&imageData, &stream);
    if (result != HSUCCEED)
    {
        logger.log(Logger::ERROR, "Failed to create image stream.");
        return faceFeature;
    }

    HFMultipleFaceData multipleFaceData = {0};
    result = HFExecuteFaceTrack(session_, stream, &multipleFaceData);
    if (result != HSUCCEED)
    {
        logger.log(Logger::ERROR, "Failed to track face.");
        HFReleaseImageStream(stream);
        return faceFeature;
    }

    if (multipleFaceData.detectedNum == 0)
    {
        logger.log(Logger::ERROR, "No face detected in the image.");
        HFReleaseImageStream(stream);
        return faceFeature;
    }

    result = HFFaceFeatureExtract(session_, stream, multipleFaceData.tokens[0], &faceFeature);
    HFReleaseImageStream(stream);

    if (result != HSUCCEED)
    {
        logger.log(Logger::ERROR, "Failed to extract face feature.");
        return faceFeature;
    }

    logger.log(Logger::INFO, "Successfully extracted face feature.");
    return faceFeature;
}

void FaceFeatureExtractor::extractAndProcessFeatures(const cv::Mat &image, const std::string &cameraId, IndexManager &indexManager, Broker *broker)
{
    Logger &logger = Logger::getInstance();

    if (image.empty())
    {
        logger.log(Logger::ERROR, "Provided image is empty.");
        return;
    }

    HFImageData imageData = {0};
    imageData.data = image.data;
    imageData.format = HF_STREAM_BGR;
    imageData.height = image.rows;
    imageData.width = image.cols;
    imageData.rotation = HF_CAMERA_ROTATION_0;

    HFImageStream stream;
    HResult result = HFCreateImageStream(&imageData, &stream);
    if (result != HSUCCEED)
    {
        logger.log(Logger::ERROR, "Failed to create image stream.");
        return;
    }

    HFMultipleFaceData multipleFaceData = {0};
    result = HFExecuteFaceTrack(session_, stream, &multipleFaceData);
    if (result != HSUCCEED)
    {
        logger.log(Logger::ERROR, "Failed to track face.");
        HFReleaseImageStream(stream);
        return;
    }

    if (multipleFaceData.detectedNum == 0)
    {

        HFReleaseImageStream(stream);
        return;
    }
    auto customOption = HF_ENABLE_QUALITY | HF_ENABLE_LIVENESS;
    result = HFMultipleFacePipelineProcessOptional(session_, stream, &multipleFaceData, customOption);
    if (result != HSUCCEED)
    {
        logger.log(Logger::ERROR, "Failed to multiple face pipeline process.");
        HFReleaseImageStream(stream);
        return;
    }
    HFFaceQualityConfidence qualityConfidence = {0};
    HFGetFaceQualityConfidence(session_, &qualityConfidence);
    for (int i = 0; i < multipleFaceData.detectedNum; ++i)
    {
        HFFaceFeature faceFeature = {0};
        result = HFFaceFeatureExtract(session_, stream, multipleFaceData.tokens[i], &faceFeature);

        if (result == HSUCCEED)
        {

            std::pair<std::string, float> searchResult = indexManager.searchIndex(faceFeature);
            std::string message = cameraId + ":" + searchResult.first + ":" + std::to_string(searchResult.second) + ":" + std::to_string(qualityConfidence.confidence[i]);
            broker->sendMessage(message);
        }
        else
        {
            logger.log(Logger::ERROR, "Failed to extract face feature for face " + std::to_string(i));
        }
    }

    HFReleaseImageStream(stream);
    return;
}
