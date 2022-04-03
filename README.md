
# 🔐 AR as a Service


[![Code style: black](https://img.shields.io/badge/code%20style-black-000000.svg)](https://github.com/psf/black)


An authentication library strongly built in Python (Django and Django Rest Framework). It serves the purpose of quick bootstrapping a project's authentication infrastructure.



Abstract
-----------
A reliable and trustworthy authentication library made for anyone who's a tinkerer and wants to get their personal or professional project authentication infrastructure built in no time.

![djangorest-routes](https://user-images.githubusercontent.com/55067204/161224355-7a6c59cc-9d14-4a9c-a861-19f2e7682688.png)


Routes
---------
Here are it's key features:

- register
- login (jwt)
- login (refresh jwt)
- confirm otp 
- resend otp code
- logout
- change password
- reset password otp (otp)
- reset password otp confirm (otp)
- reset password otp complete (otp)
- suspend user (not completed)


Requirements
---------------

* Python (3.6, 3.7, 3.8, 3.9, 3.10)
* Django (2.2, 3.0, 3.1, 3.2, 4.0)


Quick Start
-----------

1. Install using `pip`:
```
    pip install djangorest-routes
```

2. Add "djangorest_routes" to your INSTALLED_APPS setting:
```
    INSTALLED_APPS = [
        ...
        'rest_routes',
    ]
```

3. Set "rest_routes.User" to AUTH_USER_MODEL setting:
```
AUTH_USER_MODEL = "rest_routes.User"
```

4. Set the length of the OTP code in your project settings, default is `6`:
```
OTP_LENGTH = 8
```

5. Include the OTP salt key in your project settings, do not expose this salt key:
```
SALT_KEY = "some-secured-salt-key-for-otp-hashing"
```

6. Include the polls URLconf in your project urls.py:
```
    path('rest_routes/', include('rest_routes.urls')),
```

7. Run ``python manage.py migrate`` to create the `djangorest_routes` models.

8. Start the development server and visit http://127.0.0.1:8000/admin/

9. Visit http://127.0.0.1:8000/rest_routes/ to test the authentication logics.


Documentation & Support
--------------------------

Full documentation for the project is available at [docs](https://djangorest-auth.digitalstade.com/).

You may also want to follow the author on [twitter](https://twitter.com/israelabraham_).


License
---------
Disclaimer: Everything you see here is open and free to use as long as you comply with the [license](https://github.com/israelabraham/djangorest-routes/blob/main/LICENSE.txt). There are no hidden charges. We promise to do our best to fix bugs and improve the code.


Gratitude
----------
Special thanks goes to the beautiful brains of the below listed packages. From your works, I tinkered and came up with something that works best for me! I'll forever be grateful!

- [django](https://github.com/django/django)
- [djangorestframework](https://github.com/encode/django-rest-framework)
- [djangorestframework-simplejwt](https://github.com/jazzband/djangorestframework-simplejwt)
- [rest-api-payload](https://github.com/israelabraham/api-payload)
