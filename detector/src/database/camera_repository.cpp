#include "database/camera_repository.h"
#include "utils/logger.h"

CameraRepository::CameraRepository() : Database() {}

CameraRepository::~CameraRepository() {}

std::vector<Camera> CameraRepository::mapDatabaseResultToCameras(const pqxx::result &result)
{
    std::vector<Camera> cameras;

    for (const auto &row : result)
    {

        Camera camera(row["id"].as<std::string>(),
                      row["ip"].as<std::string>(),
                      row["password"].as<std::string>());
        cameras.push_back(camera);
    }

    return cameras;
}

std::vector<Camera> CameraRepository::fetchCameras()
{
    Logger &logger = Logger::getInstance();
    std::vector<Camera> cameras;

    if (!connection || !connection->is_open())
    {
        logger.log(Logger::ERROR, "Database connection is not open.");
        return cameras;
    }

    try
    {
        pqxx::work transaction(*connection);
        pqxx::result result = transaction.exec("SELECT id, ip, password FROM cameras");

        cameras = mapDatabaseResultToCameras(result);
        transaction.commit();

        logger.log(Logger::INFO, "Successfully fetched " + std::to_string(cameras.size()) + " cameras from the database.");
    }
    catch (const std::exception &exception)
    {
        logger.log(Logger::ERROR, "Error fetching cameras: " + std::string(exception.what()));
    }

    return cameras;
}
