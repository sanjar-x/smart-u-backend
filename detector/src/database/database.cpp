#include "database/database.h"
#include <iostream>

Database::Database() : connection(nullptr)
{
    Logger &logger = Logger::getInstance();
    try
    {
        connection = new pqxx::connection(connection_options);
        if (connection->is_open())
        {
            std::string dbname = connection->dbname();
            logger.log(Logger::INFO, "Connected to database: " + dbname);
        }
        else
        {
            logger.log(Logger::ERROR, "Failed to connect to database.");
            delete connection;
            connection = nullptr;
        }
    }
    catch (const std::exception &exception)
    {
        logger.log(Logger::ERROR, exception.what());
        connection = nullptr;
    }
}

Database::~Database()
{
    if (connection)
    {
        connection->disconnect();
        delete connection;
    }
}
