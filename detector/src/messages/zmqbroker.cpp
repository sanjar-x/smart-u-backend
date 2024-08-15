#include <iostream>
#include "messages/zmqbroker.h"

Broker::Broker(const std::string &endpoint)
    : context_(1), socket_(context_, zmq::socket_type::pair)
{
    socket_.bind(endpoint);
}

void Broker::sendMessage(const std::string &message)
{
    zmq::message_t zmq_message(message.begin(), message.end());
    socket_.send(zmq_message, zmq::send_flags::none);
}