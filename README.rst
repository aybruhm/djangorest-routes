===================
Django Rest Auth
===================

A simple installable Django Rest Authentication package.

Detailed documentation is in the "docs" directory.

Quick start
-----------

1. Add "djangorest_auth" to your INSTALLED_APPS setting like this::

    INSTALLED_APPS = [
        ...
        'djangorest_auth',
    ]

2. Include the polls URLconf in your project urls.py like this::

    path('rest_auth/', include('djangorest_auth.urls')),

3. Run ``python manage.py migrate`` to create the djangorest_auth models.

4. Start the development server and visit http://127.0.0.1:8000/admin/

5. Visit http://127.0.0.1:8000/rest_auth/ to test the authentication logics.