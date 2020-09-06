import os
import secrets
from PIL import Image
from flask import url_for,current_app
from flaskblog import mail
from flask_mail import Message



def save_picture(form_picture):
    random_hex = secrets.token_hex(8)
    _, f_ext = os.path.splitext(form_picture.filename)
    picture_fn = random_hex + f_ext
    picture_path = os.path.join(current_app.root_path, 'static/profile_pics', picture_fn)

    output_size = (125, 125)
    i = Image.open(form_picture)
    i.thumbnail(output_size)
    i.save(picture_path)

    return picture_fn



def send_email(user):
    msg = Message('Passwords Reset',
                  sender='noreply@demo.com',
                  recipients = [user.email])
    msg.body = f'''
    To reset yout password please follow link:
    {url_for('users.reset_password',token=user.get_reset_token(),_external=True)}
    '''
    mail.send(msg)