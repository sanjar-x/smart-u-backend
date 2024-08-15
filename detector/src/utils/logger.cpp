#include "utils/logger.h"

Logger &Logger::getInstance()
{
    static Logger instance;
    return instance;
}

Logger::Logger() {}

Logger::~Logger() {}

void Logger::log(LogLevel level, const std::string &message)
{
    std::lock_guard<std::mutex> lock(logMutex);

    std::string levelStr = getLogLevelString(level);
    std::cout << "[" << levelStr << "] " << message << std::endl;
    // Вы также можете добавить запись в файл или другую систему логирования здесь.
}

std::string Logger::getLogLevelString(LogLevel level)
{
    switch (level)
    {
    case INFO:
        return "INFO";
    case WARNING:
        return "WARNING";
    case ERROR:
        return "ERROR";
    default:
        return "UNKNOWN";
    }
}
