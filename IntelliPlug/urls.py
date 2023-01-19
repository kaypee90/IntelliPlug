"""IntelliPlug URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/1.11/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  url(r'^$', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  url(r'^$', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.conf.urls import url, include
    2. Add a URL to urlpatterns:  url(r'^blog/', include('blog.urls'))
"""
from django.conf.urls import url, include
from django.contrib import admin
from django.conf import settings
from rest_framework.routers import DefaultRouter
from intelliroute import views

admin.site.site_header = "Intelli-Route"
admin.site.site_title = "Welcome to Intelli-Route"
admin.site.index_title = "Intelli-Route"

router = DefaultRouter()
router.register(r"integrating_apps", views.IntegratingAppViewSet)
router.register(r"request_audits", views.RequestAuditViewSet)

urlpatterns = [
    url(r"^grappelli/", include("grappelli.urls")),
    url(r"^", include(router.urls)),
    url(r"^intelliroute/$", views.IntelliRouteList.as_view()),
    url(r"^intelliroute/(?P<pk>[0-9]+)/$", views.IntelliRouteDetail.as_view()),
    url(r"^admin/", admin.site.urls),
]

if settings.DEBUG and "debug_toolbar" in settings.INSTALLED_APPS:
    import debug_toolbar

    urlpatterns = [
        url("__debug__/", include(debug_toolbar.urls)),
        # For django versions before 2.0:
        # url(r'^__debug__/', include(debug_toolbar.urls)),
    ] + urlpatterns
