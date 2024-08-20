// streamer.h
#pragma once

#include <vector>
#include <queue>
#include <thread>
#include <mutex>
#include <condition_variable>
#include "camera.h"
#include "video/stream.h"
#include "face_feature_extractor.h"
#include "index_manager.h"
#include "messages/zmqbroker.h"

class Streamer
{
public:
    Streamer(std::vector<Camera> cameras,
             IndexManager &indexManager,
             const std::string &brokerEndpoint);

    void processStreams();

private:
    std::vector<Stream> streams_;
    IndexManager &indexManager_;
    Broker broker_;
    std::queue<Stream *> capture_queue_;
    std::mutex queue_mutex_;
    std::condition_variable cv_;

    static const int NUM_THREADS = 12;

    void openStreams(std::vector<Camera> cameras);
    void processStream(Stream &stream, FaceFeatureExtractor &faceFeatureExtractor);
};