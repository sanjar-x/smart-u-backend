#include "index_manager.h"
#include "utils/logger.h"
#include "database/image_repository.h"
#include "inspireface/face_feature_extractor.h"

IndexManager::IndexManager() : index_(std::make_unique<faiss::IndexFlatL2>(512)) {}

IndexManager::~IndexManager() = default;

void IndexManager::buildIndex()
{

    Logger &logger = Logger::getInstance();
    ImageRepository imageRepository;

    std::pair<std::vector<std::string>, std::vector<cv::Mat>> loadedImages = imageRepository.loadImages();
    const std::vector<std::string> &ids = loadedImages.first;
    const std::vector<cv::Mat> &images = loadedImages.second;
    FaceFeatureExtractor faceFeatureExtractor;

    for (size_t i = 0; i < images.size(); ++i)
    {
        HFFaceFeature feature = faceFeatureExtractor.extractFeature(images[i]);
        logger.log(Logger::INFO, "Adding feature ID: " + ids[i] + " to the index.");
        index_->add(1, feature.data);
        featureIds_.push_back(ids[i]);
    }
    std::int64_t total = index_->ntotal;
    logger.log(Logger::INFO, "Total elements in index: " + std::to_string(total));
}

std::pair<std::string, float> IndexManager::searchIndex(const HFFaceFeature &queryFeature)
{
    Logger &logger = Logger::getInstance();

    std::vector<float> distances(1);
    std::vector<int64_t> indices(1);
    index_->search(1, queryFeature.data, 1, distances.data(), indices.data());
    if (indices[0] >= 0 && indices[0] < featureIds_.size())
    {
        return {featureIds_[indices[0]], distances[0]};
    }
    else
    {
        logger.log(Logger::ERROR, "Search result out of bounds.");
        return {"", std::numeric_limits<float>::max()};
    }
}
