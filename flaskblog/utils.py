import os
import secrets
from PIL import Image
from flaskblog import app
from flask import current_app
from flask_login import current_user
import random
import shutil

def save_picture(form_picture):
    random_hex = secrets.token_hex(16)
    _, f_ext = os.path.splitext(form_picture.filename)
    picture_fn = random_hex + f_ext
    full_path = os.path.join(current_app.root_path, 'static', 'profile_pics/', current_user.username, 'account_img')
    if not os.path.exists(full_path):
        os.mkdir(full_path)
    picture_path = os.path.join(full_path, picture_fn)
    output_size = (125, 125)
    i = Image.open(form_picture)
    i.thumbnail(output_size)
    i.save(picture_path)
    return picture_fn

def save_picture_post(form_postpicture):
    random_hex = secrets.token_hex(16)
    _, f_ext = os.path.splitext(form_postpicture.filename)
    picture_fn = random_hex + f_ext
    full_path = os.path.join(current_app.root_path, 'static', 'profile_pics/', current_user.username, 'post_images')
    if not os.path.exists(full_path):
        os.mkdir(full_path)
    picture_path = os.path.join(full_path, picture_fn)
    output_size = (320, 320)
    i = Image.open(form_postpicture)
    i.thumbnail(output_size)
    i.save(picture_path)

    return picture_fn

def random_avatar(user):
    full_path = os.path.join(os.getcwd(), 'flaskblog/static', 'profile_pics' , user, 'account_img')
    if not os.path.exists(full_path):
        os.makedirs(full_path)
    full_path_avatar = os.path.join(os.getcwd(), 'flaskblog/static/profile_pics/Avatars/')
    list_avatars = os.listdir(full_path_avatar)
    lst = random.choice(list_avatars)
    random_image_file = os.path.join(full_path_avatar, lst)
    shutil.copy(random_image_file, full_path)
    return lst