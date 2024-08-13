#pragma once
#include "inspireface/intypedef.h"
#include "inspireface/herror.h"
#include "inspireface/inspireface.h"

class Session
{
public:
    Session();
    ~Session();

    HFSession getSession(HFSessionCustomParameter parameter, HFDetectMode detectMode, HInt32 maxDetectFaceNum, HInt32 detectPixelLevel, HInt32 trackByDetectModeFPS);
    HResult releaseSession();

private:
    HFSession session;
};
