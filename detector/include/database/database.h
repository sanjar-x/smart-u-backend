#pragma once
#include <string>
#include <pqxx/pqxx>
#include "utils/logger.h"

class Database
{
public:
    Database();
    ~Database();

protected:
    pqxx::connection *connection;
    std::string connection_options = "dbname=smart-u user=root password=textile9495 hostaddr=127.0.0.1 port=5432";
};
