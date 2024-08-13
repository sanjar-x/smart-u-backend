#ifndef ZMQ_MANAGER_H
#define ZMQ_MANAGER_H

#include <zmq.hpp>
#include <string>
#include <vector>
#include <mutex>

class ZMQManager
{
public:
    static ZMQManager &getInstance()
    {
        static ZMQManager instance;
        return instance;
    }

    void sendMessage(const std::string &message)
    {
        std::lock_guard<std::mutex> lock(mutex_);
        zmq::message_t zmq_message(message.size());

        memcpy(zmq_message.data(), message.c_str(), message.size());
        socket_.send(zmq_message, zmq::send_flags::none);
    }

    void sendMessages(const std::vector<std::string> &data)
    {
        std::lock_guard<std::mutex> lock(mutex_);
        std::vector<char> serialized;

        for (const auto &msg : data)
        {
            serialized.insert(serialized.end(), msg.begin(), msg.end());
            serialized.push_back('\0'); // Null terminator as delimiter
        }

        zmq::message_t iter_message(serialized.begin(), serialized.end());
        socket_.send(iter_message, zmq::send_flags::none);
    }

private:
    ZMQManager() : context_(1), socket_(context_, ZMQ_PUSH)
    {
        socket_.connect("tcp://localhost:5555");
    }
    ZMQManager(const ZMQManager &) = delete;
    ZMQManager &operator=(const ZMQManager &) = delete;

    zmq::context_t context_;
    zmq::socket_t socket_;
    std::mutex mutex_;
};

#endif // ZMQ_MANAGER_H
