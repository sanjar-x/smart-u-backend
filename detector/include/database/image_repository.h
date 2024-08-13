#pragma once
#include "database/database.h"
#include "utils/logger.h"
#include <vector>
#include <string>

class Image
{
public:
    std::string id;
    std::string file_name;
};

class ImageRepository : public Database
{
public:
    ImageRepository();
    ~ImageRepository();

    std::vector<Image> getImages();

private:
    std::vector<Image> parseImages(const pqxx::result &result);
};
