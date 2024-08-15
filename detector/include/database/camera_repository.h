#pragma once

#include <vector>
#include <string>
#include "video/camera.h"
#include "database.h"

class CameraRepository : public Database
{
public:
    CameraRepository();
    ~CameraRepository();

    std::vector<Camera> fetchCameras();

private:
    std::vector<Camera> mapDatabaseResultToCameras(const pqxx::result &result);
};
