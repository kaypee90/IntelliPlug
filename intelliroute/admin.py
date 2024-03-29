from django.contrib import admin
from reversion.admin import VersionAdmin
from intelliroute.models import IntegratingApp, RequestAudit


class IntegratingAppAdmin(VersionAdmin):
    date_hierarchy = "created_at"
    search_fields = ["name", "alias"]
    list_display = ["name", "alias", "base_url", "created_at", "updated_at", "status"]


class RequestAuditAdmin(VersionAdmin):
    date_hierarchy = "created_at"
    search_fields = ["http_method", "integrating_app__name"]
    list_display = [
        "integrating_app__name",
        "http_method",
        "request_url",
        "response_code",
        "response_time",
        "created_at",
    ]


admin.site.register(IntegratingApp, IntegratingAppAdmin)
admin.site.register(RequestAudit, RequestAuditAdmin)
