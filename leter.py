#  Напиш синхронизатор который по заросы извлекает


#     while True:
#         counter += 1
#         string = await socket.recv_string()
#         timestamp = time.time()
#         data = string.split(":")
#         await r.zadd(
#             f"detections:camera:{data[1]}:user:{data[3]}", {f"{timestamp}": timestamp}
#         )

#         redis_key = f"detections:camera:{camera_id}:user:{user_id}"
#         redis_timestamps = await redis.zrangebyscore(redis_key, max_timestamp, "+inf")
#   await redis.sadd(f"camera:{camera_id}:users", user_id)
#     await redis.sadd(f"user:{user_id}:cameras", camera_id)

# class Detection(Base):
#     __tablename__ = "detections"
#     id: Mapped[uuid.UUID] = mapped_column(
#         UUID(as_uuid=True), primary_key=True, default=uuid.uuid4
#     )
#     camera_id: Mapped[uuid.UUID] = mapped_column(
#         UUID(as_uuid=True), ForeignKey("cameras.id", ondelete="SET NULL")
#     )
#     user_id: Mapped[uuid.UUID] = mapped_column(
#         UUID(as_uuid=True), ForeignKey("users.id", ondelete="SET NULL")
#     )
#     time: Mapped[time] = mapped_column(TIMESTAMP)

#     async def get_max(self, session: AsyncSession):
#         result = await session.execute(select(func.max(self.__class__.time)))
#         obj = result.scalar_one_or_none()
#         return await self._setattr_instance(obj)


# r = redis.Redis(host="localhost", port=6379, db=0)
# r.sadd(f"camera:{camera_id}:users", user_id)

# r.sadd(f"user:{user_id}:cameras", camera_id)


# @scheduler.scheduled_job("interval", seconds=10)
# def synchronizer():
#     print("scheduled_job_1")
