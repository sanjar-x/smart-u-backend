from redis.asyncio import Redis, ConnectionPool

pool = ConnectionPool(
    host="localhost", port=6379, db=0, max_connections=10, decode_responses=True
)

client = Redis(connection_pool=pool, auto_close_connection_pool=False)
