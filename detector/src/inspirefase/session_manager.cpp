#include "session_manager.h"
#include "utils/logger.h"

SessionManager::SessionManager()
{
    // Constructor can be used to initialize resources if needed
}

SessionManager::~SessionManager()
{
}

HFSession SessionManager::createSession()
{
    Logger &logger = Logger::getInstance();

    HFSession session;
    HResult result = HFCreateInspireFaceSessionOptional(customOption, detectMode, maxDetectFaceNum, detectPixelLevel, trackByDetectModeFPS, &session);
    if (result != HSUCCEED)
    {
        logger.log(Logger::ERROR, "Failed to create InspireFace session.");
        return nullptr;
    }

    result = configureSession(session);
    if (result != HSUCCEED)
    {
        logger.log(Logger::ERROR, "Failed to configure InspireFace session.");
        return nullptr;
    }

    logger.log(Logger::INFO, "InspireFace session created and configured successfully.");
    return session;
}

HResult SessionManager::releaseSession(HFSession session)
{
    Logger &logger = Logger::getInstance();

    if (session)
    {
        HResult result = HFReleaseInspireFaceSession(session);
        if (result != HSUCCEED)
        {
            logger.log(Logger::ERROR, "Failed to release InspireFace session.");
            return result;
        }
        logger.log(Logger::INFO, "InspireFace session released successfully.");
    }
    else
    {
        logger.log(Logger::INFO, "No InspireFace session to release.");
    }
    return HSUCCEED;
}

HResult SessionManager::configureSession(HFSession session)
{
    Logger &logger = Logger::getInstance();
    HResult result = HFSessionSetTrackPreviewSize(session, detectPixelLevel);
    if (result != HSUCCEED)
    {
        logger.log(Logger::ERROR, "Failed to set track preview size. DetectPixelLevel: " + std::to_string(detectPixelLevel));
        return result;
    }
    logger.log(Logger::INFO, "Track preview size set successfully. DetectPixelLevel: " + std::to_string(detectPixelLevel));

    result = HFSessionSetFilterMinimumFacePixelSize(session, minimumFacePixelSize);
    if (result != HSUCCEED)
    {
        logger.log(Logger::ERROR, "Failed to set minimum face pixel size for filter. Minimum size: " + std::to_string(minimumFacePixelSize));
        return result;
    }
    logger.log(Logger::INFO, "Minimum face pixel size for filter set successfully. Minimum size: " + std::to_string(minimumFacePixelSize));

    result = HFSessionSetFaceDetectThreshold(session, threshold);
    if (result != HSUCCEED)
    {
        logger.log(Logger::ERROR, "Failed to set face detection threshold. Threshold: " + std::to_string(threshold));
        return result;
    }
    logger.log(Logger::INFO, "Face detection threshold set successfully. Threshold: " + std::to_string(threshold));

    return HSUCCEED;
}
