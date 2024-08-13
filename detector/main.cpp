#include <iostream>
#include <thread>

#include "database/camera_repository.h"
#include "database/database.h"
#include "database/image_repository.h"
#include "index/faiss.h"
#include "inspireface/detector.h"
#include "inspireface/recogination.h"
#include "inspireface/herror.h"
#include "inspireface/inspireface.h"
#include "inspireface/intypedef.h"
#include "messages/zmqbroker.h"
#include "utils/logger.h"
#include "video/camera.h"
#include "video/streamer.h"

void logMessages(Logger &logger, int number)
{
    while (true)
    {
        logger.log(Logger::INFO, std::to_string(number) + " Thread logging");
    }
}

int main()
{
    Logger &logger = Logger::getInstance();

    logger.log(Logger::INFO, "Application started");

    std::thread t1(logMessages, std::ref(logger), 1);
    std::thread t2(logMessages, std::ref(logger), 2);

    t1.join();
    t2.join();

    logger.log(Logger::INFO, "Application ended");

    return 0;
}
