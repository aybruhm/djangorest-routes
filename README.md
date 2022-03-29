
# Authentication Routes As A Service



description::long description



Abstract
-----------
Bootstrap your single page application with this amazing rest authentication reusable app built using django/djangorestframework


**Below**: *Screenshot from the browsable API*



Requirements
---------------

* Python (3.6, 3.7, 3.8, 3.9, 3.10)
* Django (2.2, 3.0, 3.1, 3.2, 4.0)


Quick Start
-----------

1. Install using `pip`...

    pip install djangorest-auth

2. Add "djangorest_auth" to your INSTALLED_APPS setting like this::

    INSTALLED_APPS = [
        ...
        'djangorest_auth',
    ]

2. Include the polls URLconf in your project urls.py like this::

    path('rest_auth/', include('djangorest_auth.urls')),

4. Run ``python manage.py migrate`` to create the djangorest_auth models.

5. Start the development server and visit http://127.0.0.1:8000/admin/

6. Visit http://127.0.0.1:8000/rest_auth/ to test the authentication logics.


Documentation & Support
--------------------------

Full documentation for the project is available at [https://www.django-rest-framework.org/][docs].

For questions and support, use the [REST framework discussion group][group], or `#restframework` on libera.chat IRC.

You may also want to [follow the author on Twitter][twitter].