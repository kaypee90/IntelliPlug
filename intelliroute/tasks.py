from __future__ import absolute_import, unicode_literals
from celery import shared_task
from intelliroute.utils import create_request_audit


@shared_task
def add_audit_to_database(
    http_method, request_url, response_time, response_code, integrating_app_id
):
    create_request_audit(
        http_method, request_url, response_time, response_code, integrating_app_id
    )
    return True
