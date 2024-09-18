import os
import secrets
from PIL import Image
from flaskblog import app

def save_picture(form_picture):
    random_hex = secrets.token_hex(8)
    _, f_ext = os.path.splitext(form_picture.filename)
    picture_fn = random_hex + f_ext
    picture_path = os.path.join(app.root_path, 'static/profile_pics', picture_fn)

    output_size = (125, 125)
    i = Image.open(form_picture)
    i.thumbnail(output_size)
    i.save(picture_path)

    return picture_fn

def save_picture_post(form_postpicture):
    random_hex = secrets.token_hex(8)
    _, f_ext = os.path.splitext(form_postpicture.filename)
    picture_fn = random_hex + f_ext
    picture_path = os.path.join(app.root_path, 'static/post_pics', picture_fn)

    output_size = (320, 320)
    i = Image.open(form_postpicture)
    i.thumbnail(output_size)
    i.save(picture_path)

    return picture_fn

