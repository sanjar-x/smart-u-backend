#include "inspireface/intypedef.h"
#include "inspireface/herror.h"
#include "inspireface/inspireface.h"
#include "inspireface/session.h"
#include "utils/logger.h"

Session::Session() : session(nullptr) {}

Session::~Session()
{
    releaseSession();
}

HFSession Session::getSession(HFSessionCustomParameter parameter, HFDetectMode detectMode, HInt32 maxDetectFaceNum, HInt32 detectPixelLevel, HInt32 trackByDetectModeFPS)
{
    Logger &logger = Logger::getInstance();

    if (!session)
    {
        HOption option = HF_ENABLE_FACE_RECOGNITION | HF_ENABLE_QUALITY | HF_ENABLE_LIVENESS | HF_ENABLE_FACE_ATTRIBUTE | HF_ENABLE_INTERACTION;
        HResult result = HFCreateInspireFaceSessionOptional(option, HF_DETECT_MODE_ALWAYS_DETECT, maxDetectFaceNum, detectPixelLevel, trackByDetectModeFPS, &session);
        if (result != HSUCCEED)
        {
            logger.log(Logger::ERROR, "Failed to create InspireFace session.");
            return nullptr;
        }
        logger.log(Logger::INFO, "InspireFace session created successfully.");
        HResult result = HFSessionSetFilterMinimumFacePixelSize(session, 24);
        if (result != HSUCCEED)
        {
            logger.log(Logger::ERROR, "Failed to set filter minimum face pixel size at session.");
            return nullptr;
        }
    }
    HResult result = HFSessionSetFilterMinimumFacePixelSize(session, 24);
    return session;
}

HResult Session::releaseSession()
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
        session = nullptr;
        logger.log(Logger::INFO, "InspireFace session released successfully.");
        return HSUCCEED;
    }
    logger.log(Logger::INFO, "No InspireFace session to release.");
    return HSUCCEED;
}
