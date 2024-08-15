#pragma once
#include "inspireface/intypedef.h"
#include "inspireface/herror.h"
#include "inspireface/inspireface.h"

class SessionManager
{
public:
    SessionManager();
    ~SessionManager();

    HOption customOption = HF_ENABLE_FACE_RECOGNITION | HF_ENABLE_QUALITY | HF_ENABLE_LIVENESS | HF_ENABLE_FACE_ATTRIBUTE | HF_ENABLE_INTERACTION;
    HFDetectMode detectMode = HF_DETECT_MODE_ALWAYS_DETECT;
    HInt32 maxDetectFaceNum = 99;
    HInt32 detectPixelLevel = 640;
    HInt32 trackByDetectModeFPS = 30;
    HInt32 minimumFacePixelSize = 32;
    HFloat threshold = 0.7;

    HFSession createSession();
    HResult releaseSession(HFSession session);

private:
    HResult configureSession(HFSession session);
};
