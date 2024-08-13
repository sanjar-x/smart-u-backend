#include "logger.h"

Logger::Logger()
{
    // Конструктор по-прежнему пуст, так как логирование в файл убрано
}

Logger::~Logger()
{
    // Деструктор по-прежнему пуст
}

Logger &Logger::getInstance()
{
    static Logger instance;
    return instance;
}

void Logger::log(LogLevel level, const std::string &message)
{
    std::lock_guard<std::mutex> guard(logMutex);
    std::cout << getTime() << " [" << getLogLevelString(level) << "] " << message << std::endl;
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
