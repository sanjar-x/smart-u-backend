#ifndef LOGGER_H
#define LOGGER_H

#include <string>
#include <iostream>
#include <mutex>
#include "utils/common.h"

class Logger
{
public:
    enum LogLevel
    {
        INFO,
        WARNING,
        ERROR
    };

    static Logger &getInstance();
    void log(LogLevel level, const std::string &message);

private:
    Logger();
    ~Logger();

    std::string getLogLevelString(LogLevel level);

    std::mutex logMutex;
};

#endif // LOGGER_H
