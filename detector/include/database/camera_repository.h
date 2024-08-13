#pragma once
#include <vector>
#include "database/database.h"
#include "video/camera.h"

class CameraRepository : public Database
{
public:
    CameraRepository();
    ~CameraRepository();

    std::vector<Camera> getCameras();

private:
    std::vector<Camera> parseCameras(const pqxx::result &result);
};