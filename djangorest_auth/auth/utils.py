# -----------------------
# DJANGO APP IMPORTS
# -----------------------
from django.contrib.auth import authenticate, get_user_model
from django.conf import settings

# --------------------------------
# REST FRAMEWORK MODULE IMPORTS
# --------------------------------
from rest_framework import serializers

# --------------------------
# BUILT-IN LIBRARY IMPORTS
# --------------------------
import random
import uuid
import datetime
import jwt

# -----------------------
# EMAIL DJANGO IMPORTS
# -----------------------
from django.core.mail import send_mail, EmailMessage
from django.template.loader import render_to_string
from django.conf import settings


User = get_user_model()


def random_digits():
    return "%0.12d" % random.randint(0, 999999999999)


def get_and_authenticate_user(email, password):
    user = authenticate(username=email, password=password)

    if user is None:
        raise serializers.ValidationError(
            "Invalid email or password. Please try again!")
    return user


def create_user_account(email, password, firstname="",
                        lastname="", activation_token="", **extra_fields):
    user = User.objects.create_user(
        email=email, password=password, firstname=firstname,
        lastname=lastname, activation_token=random_digits(), ** extra_fields)
    user.is_active = True
    user.username = generate_uniquie_username()
    user.save()
    return user


def generate_uniquie_username():
    # Generates a unique username id
    unique_username = uuid.uuid4()
    # Filter user by the generated unique username id
    user = User.objects.filter(username=unique_username)

    """
    Checks if a user with the generated unique username id does not exist,
    then go ahead and set the unique username to the incoming user
    """
    if not user:
        username = unique_username
        return username
        

def generate_access_token(user):
    
    # -------------------------------------------------------
    # Wrapped user_id, expiration_date and iat to a payload
    # -------------------------------------------------------
    access_token_payload = {
        "user_id": user.id,
        "exp": datetime.datetime.utcnow() + datetime.timedelta(days=0, minutes=30),
        "iat": datetime.datetime.utcnow(),
    }
    
    # ------------------------------------------------------------------------------
    # Encode the access token payload, with the secret key and algorithm using JWT
    # ------------------------------------------------------------------------------
    access_token = jwt.encode(
        access_token_payload, 
        settings.SECRET_KEY, 
        algorithm="HS256"
    )
    
    # ----------------------------------
    # Return access token to the user
    # ----------------------------------
    return access_token

def generate_refresh_token(user):
    # -------------------------------------------------------
    # Wrapped user_id, expiration_date and iat to a payload
    # -------------------------------------------------------
    refresh_token_payload = {
        'user_id': user.id,
        'exp': datetime.datetime.utcnow() + datetime.timedelta(days=1),
        'iat': datetime.datetime.utcnow()
    }
    
    # ------------------------------------------------------------------------------
    # Encode the refres token payload, with the secret key and algorithm using JWT
    # ------------------------------------------------------------------------------
    refresh_token = jwt.encode(
        refresh_token_payload, 
        settings.REFRESH_TOKEN_SECRET, 
        algorithm='HS256'
    )
    
    # ----------------------------------
    # Return access token to the user
    # ----------------------------------
    return refresh_token


def has_controller_perm_func(user):
    """
    Checks if user is authenticated, is staff and controller permission
    """
    if bool(user.is_staff == True and user.is_active == True and user.has_controls_perm == True and user.is_authenticated == True):
        return True
    return False


def send_html_to_email(to_list, subject, template_name, context, sender=settings.DEFAULT_FROM_EMAIL):
    # Parse html to string
    msg_html = render_to_string(template_name, context)
    # Initialize a single email message which can be send to multiple recipients
    msg = EmailMessage(subject=subject, body=msg_html, from_email=sender, bcc=to_list)
    # Changes content type to text/html
    msg.content_subtype = "html" 
    # Sends email and fail silently
    return msg.send()