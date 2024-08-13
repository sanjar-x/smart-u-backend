#include "database/database.h"
#include "database/image_repository.h"

ImageRepository::ImageRepository() : Database() {}

ImageRepository::~ImageRepository() {}

std::vector<Image> ImageRepository::parseImages(const pqxx::result &result)
{
    std::vector<Image> images;

    for (const auto &db_image : result)
    {
        Image image;
        image.id = db_image["id"].as<std::string>();
        image.file_name = db_image["file_name"].as<std::string>();
        images.push_back(image);
    }

    return images;
}

std::vector<Image> ImageRepository::getImages()
{
    Logger &logger = Logger::getInstance();
    std::vector<Image> images;

    if (!connection || !connection->is_open())
    {
        logger.log(Logger::ERROR, "Database connection is not open.");
        return images;
    }

    try
    {
        pqxx::work txn(*connection);
        pqxx::result result = txn.exec("SELECT id, file_name FROM images");

        images = parseImages(result);
        txn.commit();

        logger.log(Logger::INFO, "Fetched " + std::to_string(images.size()) + " images from the database.");
    }
    catch (const std::exception &exception)
    {
        logger.log(Logger::ERROR, exception.what());
    }

    return images;
}
