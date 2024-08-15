#pragma once
#include <zmq.hpp>
#include <string>

class Broker
{
public:
    Broker(const std::string &endpoint);
    void sendMessage(const std::string &message);

private:
    zmq::context_t context_;
    zmq::socket_t socket_;
};
