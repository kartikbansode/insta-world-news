from instagrapi import Client
import os

USERNAME = os.getenv("IG_USERNAME")
PASSWORD = os.getenv("IG_PASSWORD")

def post_to_instagram(image_path, caption):
    cl = Client()

    cl.login(USERNAME, PASSWORD)

    cl.photo_upload(
        image_path,
        caption
    )
