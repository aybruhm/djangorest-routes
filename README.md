
# Authentication Routes As A Service


[![Code style: black](https://img.shields.io/badge/code%20style-black-000000.svg)](https://github.com/psf/black)


description::long description



Abstract
-----------
Bootstrap your single page application with this amazing rest authentication reusable app built using django/djangorestframework


![routes](https://user-images.githubusercontent.com/55067204/160565837-3f022306-f1f5-4de4-b7c2-430679f209e1.png)


Routes
---------
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
- suspend user


Requirements
---------------

* Python (3.6, 3.7, 3.8, 3.9, 3.10)
* Django (2.2, 3.0, 3.1, 3.2, 4.0)


Quick Start
-----------

1. Install using `pip`:
```
    pip install djangorest-auth
```

2. Add "djangorest_auth" to your INSTALLED_APPS setting like this:
```
    INSTALLED_APPS = [
        ...
        'djangorest_auth',
    ]
```

2. Include the polls URLconf in your project urls.py like this:
```
    path('rest_auth/', include('djangorest_auth.urls')),
```

4. Run ``python manage.py migrate`` to create the djangorest_auth models.

5. Start the development server and visit http://127.0.0.1:8000/admin/

6. Visit http://127.0.0.1:8000/rest_auth/ to test the authentication logics.


Documentation & Support
--------------------------

Full documentation for the project is available at [docs](https://djangorest-auth.digitalstade.com/).

You may also want to follow the author on [twitter](https://twitter.com/israelabraham_).


License
---------
Disclaimer: Everything you see here is open and free to use as long as you comply with the [license](https://github.com/israelabraham/djangorest-auth/blob/main/LICENSE.txt). There are no hidden charges. We promise to do our best to fix bugs and improve the code.