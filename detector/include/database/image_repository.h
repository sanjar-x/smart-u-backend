#pragma once
#include <vector>
#include <string>
#include <opencv2/opencv.hpp>
#include "database/database.h"
#include "utils/logger.h"

struct ImageRecord
{
    std::string id;
    std::string filename;
};

class ImageRepository : public Database
{
public:
    ImageRepository();
    ~ImageRepository();

    std::vector<ImageRecord> fetchImageRecords();
    std::pair<std::vector<std::string>, std::vector<cv::Mat>> loadImages();

private:
    std::vector<ImageRecord> mapDatabaseResultToImageRecords(const pqxx::result &result);
};
