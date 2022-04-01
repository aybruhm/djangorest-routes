
# 🔐 AR as a Service


[![Code style: black](https://img.shields.io/badge/code%20style-black-000000.svg)](https://github.com/psf/black)


An authentication library strongly built in Python (Django and Django Rest Framework). It serves the purpose of quick bootstrapping a project's authentication infrastructure.



Abstract
-----------
A reliable and trustworthy authentication library made for anyone who's a tinkerer and wants to get their personal or professional project authentication infrastructure built in no time.


![routes](https://user-images.githubusercontent.com/55067204/160565837-3f022306-f1f5-4de4-b7c2-430679f209e1.png)


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
- reset password (token)
- reset password confirm (token)
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

2. Add "djangorest_routes" to your INSTALLED_APPS setting like this:
```
    INSTALLED_APPS = [
        ...
        'rest_routes',
    ]
```

2. Include the polls URLconf in your project urls.py like this:
```
    path('rest_routes/', include('rest_routes.urls')),
```

4. Run ``python manage.py migrate`` to create the djangorest-auth-as-service models.

5. Start the development server and visit http://127.0.0.1:8000/admin/

6. Visit http://127.0.0.1:8000/rest_routes/ to test the authentication logics.


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
- [django-rest-passwordreset](https://github.com/anexia-it/django-rest-passwordreset)
- [rest-api-payload](https://github.com/israelabraham/api-payload)