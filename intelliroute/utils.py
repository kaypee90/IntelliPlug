from intelliroute.models import RequestAudit, IntegratingApp

def create_request_audit(http_method, request_url, response_time, response_code, integrating_app_id):
    integrating_app = IntegratingApp.objects.get(pk=integrating_app_id)
    return RequestAudit.objects.create(http_method = http_method,
                                        request_url = request_url,
                                        response_time = response_time,
                                        response_code = response_code,
                                        integrating_app = integrating_app)