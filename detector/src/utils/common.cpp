#include "utils/common.h"

std::string getTime()
{
    std::time_t now = std::time(0);
    std::tm *localTime = std::localtime(&now);
    std::ostringstream oss;
    oss << 1900 + localTime->tm_year << "-"
        << 1 + localTime->tm_mon << "-"
        << localTime->tm_mday << " "
        << localTime->tm_hour << ":"
        << localTime->tm_min << ":"
        << localTime->tm_sec;
    return oss.str();
}
