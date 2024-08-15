#include "database/image_repository.h"
#include <opencv2/opencv.hpp>

ImageRepository::ImageRepository() : Database() {}

ImageRepository::~ImageRepository() {}

std::vector<ImageRecord> ImageRepository::mapDatabaseResultToImageRecords(const pqxx::result &result)
{
    std::vector<ImageRecord> imageRecords;

    for (const auto &row : result)
    {
        ImageRecord imageRecord;
        imageRecord.id = row["id"].as<std::string>();
        imageRecord.filename = row["file_name"].as<std::string>();
        imageRecords.push_back(imageRecord);
    }

    return imageRecords;
}

std::vector<ImageRecord> ImageRepository::fetchImageRecords()
{
    Logger &logger = Logger::getInstance();
    std::vector<ImageRecord> imageRecords;

    if (!connection || !connection->is_open())
    {
        logger.log(Logger::ERROR, "Database connection is not open.");
        return imageRecords;
    }

    try
    {
        pqxx::work transaction(*connection);
        pqxx::result result = transaction.exec("SELECT id, file_name FROM image");

        imageRecords = mapDatabaseResultToImageRecords(result);
        transaction.commit();

        logger.log(Logger::INFO, "Successfully fetched " + std::to_string(imageRecords.size()) + " image records from the database.");
    }
    catch (const std::exception &exception)
    {
        logger.log(Logger::ERROR, "Error fetching image records: " + std::string(exception.what()));
    }

    return imageRecords;
}

std::pair<std::vector<std::string>, std::vector<cv::Mat>> ImageRepository::loadImages()
{
    Logger &logger = Logger::getInstance();
    std::vector<std::string> imageIds;
    std::vector<cv::Mat> imageMats;
    std::vector<ImageRecord> imageRecords = fetchImageRecords();

    for (const auto &record : imageRecords)
    {
        cv::Mat image = cv::imread("/home/ocean/Desktop/smart-u-backend/static/users/" + record.filename, cv::IMREAD_COLOR);
        if (image.empty())
        {
            logger.log(Logger::ERROR, "Failed to load image: " + record.filename);
            continue;
        }
        imageIds.push_back(record.id);
        imageMats.push_back(image);
        logger.log(Logger::INFO, "Successfully loaded image: " + record.filename + " with ID: " + record.id);
    }

    return std::make_pair(imageIds, imageMats);
}
