#pragma once
#include <faiss/IndexFlat.h>
#include <string>
#include <vector>
#include <memory>
#include "inspireface/inspireface.h"
class IndexManager
{
public:
    IndexManager();
    ~IndexManager();

    void buildIndex();
    std::pair<std::string, float> searchIndex(const HFFaceFeature &queryFeature);

private:
    std::unique_ptr<faiss::IndexFlatL2> index_;
    std::vector<std::string> featureIds_;
};
