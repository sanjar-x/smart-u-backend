// streamer.cpp
#include "video/streamer.h"
#include <iostream>

Streamer::Streamer(std::vector<Camera> cameras,
                   IndexManager &indexManager,
                   const std::string &brokerEndpoint)
    : indexManager_(indexManager),
      broker_(brokerEndpoint)
{
    openStreams(cameras);
}

void Streamer::openStreams(std::vector<Camera> cameras)
{
    for (auto &camera : cameras)
    {
        std::string gst_pipeline = "rtspsrc location=rtsp://admin:" + camera.password + "@" + camera.ip + ":554/Streaming/Channels/101 protocols=tcp timeout=10 latency=0 ! rtph265depay ! h265parse ! nvh265dec ! videoconvert ! appsink max-buffers=1 drop=true sync=false";
        Stream stream(camera, gst_pipeline);

        if (stream.isOpen())
        {
            streams_.push_back(std::move(stream));
            std::cout << "Opened stream for camera: " << camera.id << std::endl;
        }
        else
        {
            std::cerr << "Failed to open stream for camera: " << camera.id << std::endl;
        }
    }
}

void Streamer::processStreams()
{
    std::cout << "Starting stream processing..." << std::endl;

    for (auto &stream : streams_)
    {
        capture_queue_.push(&stream);
    }

    auto worker = [this]()
    {
        FaceFeatureExtractor faceFeatureExtractor;

        while (true)
        {
            Stream *stream = nullptr;
            {
                std::unique_lock<std::mutex> lock(queue_mutex_);
                cv_.wait(lock, [this]
                         { return !capture_queue_.empty(); });

                stream = capture_queue_.front();
                capture_queue_.pop();
            }

            processStream(*stream, faceFeatureExtractor);

            {
                std::unique_lock<std::mutex> lock(queue_mutex_);
                capture_queue_.push(stream);
                cv_.notify_one();
            }
        }
    };

    std::vector<std::thread> threads;
    for (int i = 0; i < NUM_THREADS; ++i)
    {
        threads.emplace_back(worker);
        std::cout << "Started thread " << i + 1 << std::endl;
    }

    for (auto &thread : threads)
    {
        if (thread.joinable())
        {
            thread.join();
        }
    }
}

void Streamer::processStream(Stream &stream, FaceFeatureExtractor &faceFeatureExtractor)
{
    cv::Mat frame;
    if (stream.capture.read(frame))
    {
        faceFeatureExtractor.extractAndProcessFeatures(frame, stream.camera.id, indexManager_, &broker_);
    }
    return;
}