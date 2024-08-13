#include "database/database.h"
#include "database/camera_repository.h"
#include "utils/logger.h"

CameraRepository::CameraRepository() : Database() {}

CameraRepository::~CameraRepository() {}

std::vector<Camera> CameraRepository::parseCameras(const pqxx::result &result)
{
    std::vector<Camera> cameras;

    for (const auto &db_camera : result)
    {
        Camera camera;
        camera.id = db_camera["id"].as<std::string>();
        camera.ip_address = db_camera["ip_address"].as<std::string>();
        camera.password = db_camera["password"].as<std::string>();
        cameras.push_back(camera);
    }

    return cameras;
}

std::vector<Camera> CameraRepository::getCameras()
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
        pqxx::work txn(*connection);
        pqxx::result result = txn.exec("SELECT id, ip_address, password FROM cameras");

        cameras = parseCameras(result);
        txn.commit();

        logger.log(Logger::INFO, "Fetched " + std::to_string(cameras.size()) + " cameras from the database.");
    }
    catch (const std::exception &exception)
    {
        logger.log(Logger::ERROR, exception.what());
    }

    return cameras;
}
