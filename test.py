data = "camera_id:5780308e-3f8f-4db9-9e6c-d07d5f61ffe9:user_id:9cb84224-7290-41f7-a417-1ce9a154740a:distance:1.793479"
import time

# print(data.split(":"))
# data = [
#     "camera_id",
#     "5780308e-3f8f-4db9-9e6c-d07d5f61ffe9",
#     "user_id",
#     "9cb84224-7290-41f7-a417-1ce9a154740a",
#     "distance",
#     "1.793479",
# ]


print(f"camera:{data[1]}:user:{data[3]}", {"time": time.time()})
