import datetime
import io
import uuid

from google.cloud import storage

from config import CLOUD_BUCKET, STAGE


def upload_image_to_bucket(image):
    if STAGE == "production":
        storage_client = storage.Client.from_service_account_json("/credentials/cloud-bucket.json")
        bucket = storage_client.bucket(CLOUD_BUCKET)
        blob = bucket.blob(f"{uuid.uuid4()}.png")
        image_bytes = io.BytesIO()
        image.save(image_bytes, format="PNG")
        image_bytes.seek(0)
        blob.upload_from_file(image_bytes)
        return blob.name
    else:
        print("Saving image to local storage")
        image_name = f"{uuid.uuid4()}.png"
        image.save(f"static/{image_name}")
        return f"static/{image_name}"


def get_download_url(image_name):
    if STAGE == "production":
        storage_client = storage.Client.from_service_account_json("/credentials/cloud-bucket.json")
        bucket = storage_client.bucket(CLOUD_BUCKET)
        return bucket.blob(image_name).generate_signed_url(
            version="v4",
            expiration=datetime.timedelta(minutes=15),
            method="GET",
        )
    else:
        return f"http://localhost:8080/{image_name}"
