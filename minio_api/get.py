
from minio import Minio
from minio.sse import SseCustomerKey

# client = Minio(
#     "play.min.io",
#     # access_key="Q3AM3UQ867SPQQA43P2F",
#     # secret_key="zuf+tfteSlswRu7BJ86wekitnifILbZam1KYY3TG",
# )


client = Minio("192.168.17.105:9009", secure=False, access_key='horhevah', secret_key='horhevah_pass')
print(client)

# Get data of an object.
try:
    print('TRY')
    response = client.get_object("memes-bucket", "main.py")
    print(response.data)
    # Read data from response.
finally:
    response.close()
    response.release_conn()

# Get data of an object of version-ID.
# try:
#     response = client.get_object(
#         "my-bucket", "my-object",
#         version_id="dfbd25b3-abec-4184-a4e8-5a35a5c1174d",
#     )
#     # Read data from response.
# finally:
#     response.close()
#     response.release_conn()
#
# # Get data of an object from offset and length.
# try:
#     response = client.get_object(
#         "my-bucket", "my-object", offset=512, length=1024,
#     )
#     # Read data from response.
# finally:
#     response.close()
#     response.release_conn()
#
# # Get data of an SSE-C encrypted object.
# try:
#     response = client.get_object(
#         "my-bucket", "my-object",
#         ssec=SseCustomerKey(b"32byteslongsecretkeymustprovided"),
#     )
#     # Read data from response.
# finally:
#     response.close()
#     response.release_conn()