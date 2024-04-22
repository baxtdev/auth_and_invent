from rest_framework import routers
from django.urls import include, path

from .yasg import urlpatterns as url_doc

from .account.endpoints import urlpatterns as accounts_urls

urlpatterns=[
    path('accounts/', include(accounts_urls)),
]

urlpatterns+=url_doc