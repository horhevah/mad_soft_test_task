from minio import Minio
from minio.error import S3Error


def main():
    # Create a client with the MinIO server playground, its access key
    # and secret key.
    client = Minio("192.168.17.105:9009",
                   secure=False,
                   access_key='memes_user',
                   secret_key='memes_pass'
        # access_key="Q3AM3UQ867SPQQA43P2F",
        # secret_key="zuf+tfteSlswRu7BJ86wekitnifILbZam1KYY3TG",
    )

    # The file to upload, change this path if needed
    source_file = "main.py"

    # The destination bucket and filename on the MinIO server
    bucket_name = "memes-bucket"
    destination_file = "main.py"

    # Make the bucket if it doesn't exist.
    found = client.bucket_exists(bucket_name)
    if not found:
        client.make_bucket(bucket_name)
        print("Created bucket", bucket_name)
    else:
        print("Bucket", bucket_name, "already exists")

    # Upload the file, renaming it in the process
    client.fput_object(
        bucket_name, destination_file, source_file,
    )
    print(
        source_file, "successfully uploaded as object",
        destination_file, "to bucket", bucket_name,
    )


if __name__ == "__main__":
    try:
        main()
    except S3Error as exc:
        print("error occurred.", exc)
