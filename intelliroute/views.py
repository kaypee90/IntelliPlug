from rest_framework import viewsets
from rest_framework.views import APIView
from rest_framework.response import Response
from django.shortcuts import get_object_or_404
from intelliroute.serializers import (
    IntegratingAppSerializer,
    RequestAuditSerializer,
    IntelliRouteSerializer,
)
from intelliroute.models import IntegratingApp, RequestAudit
from intelliroute.tasks import add_audit_to_database
import requests
import logging
import json

logger = logging.getLogger(__name__)


JSON_CONTENT_TYPE = "application/json"


class IntegratingAppViewSet(viewsets.ModelViewSet):
    queryset = IntegratingApp.objects.all()
    serializer_class = IntegratingAppSerializer


class RequestAuditViewSet(viewsets.ModelViewSet):
    queryset = RequestAudit.objects.all()
    serializer_class = RequestAuditSerializer


class IntelliRouteList(APIView):
    """
    Routes a GET all or POST requests
    """

    def get(self, request, format=None):
        ALIAS = "alias"
        RESOURCE = "resource"
        HTTP_METHOD = "GET"
        headers = {"Content-Type": JSON_CONTENT_TYPE, "Accept": JSON_CONTENT_TYPE}

        logger.info("====================================================")
        alias = request.GET.get(ALIAS)
        resource = request.GET.get(RESOURCE)
        query_string = request.META.get("QUERY_STRING")
        logger.info(alias)
        logger.info(resource)
        logger.info(query_string)

        obj_integration_app = get_object_or_404(IntegratingApp, alias=alias)
        URL = obj_integration_app.base_url

        if resource:
            URL = URL + resource + "/"
        if query_string:
            URL = URL + "?" + query_string

        response = requests.get(URL, headers=headers)
        logger.info("====================================================")
        logger.info(URL)
        logger.info("====================================================")
        logger.info(response.elapsed.total_seconds())
        logger.info(response.status_code)
        logger.info(response.headers)
        logger.info("====================================================")

        add_audit_to_database.delay(
            http_method=HTTP_METHOD,
            request_url=response.url,
            response_time=response.elapsed.total_seconds(),
            response_code=response.status_code,
            integrating_app_id=obj_integration_app.pk,
        )
        if not response.ok:
            logger.error("GET request failed")
            return Response({"message": response.text}, status=response.status_code)

        if JSON_CONTENT_TYPE not in response.headers.get("Content-Type"):
            return Response(
                {
                    "message": "The response content type {} is not supported.".format(
                        response.headers.get("Content-Type")
                    )
                },
                status=403,
            )

        json_response = response.json()
        if not json_response:
            json_response = {"data": None}
        else:
            json_response = {"data": json_response}

        serializer = IntelliRouteSerializer(json_response)
        return Response(serializer.data, status=response.status_code)

    def post(self, request, format=None):
        ALIAS = "alias"
        RESOURCE = "resource"
        HTTP_METHOD = "POST"
        headers = {"Content-Type": JSON_CONTENT_TYPE}

        logger.info("====================================================")
        alias = request.GET.get(ALIAS)
        resource = request.GET.get(RESOURCE)
        query_string = request.META.get("QUERY_STRING")
        logger.info(alias)
        logger.info(resource)
        logger.info(query_string)

        obj_integration_app = get_object_or_404(IntegratingApp, alias=alias)
        URL = obj_integration_app.base_url

        if resource:
            URL = URL + resource + "/"
        if query_string:
            URL = URL + "?" + query_string

        payload = json.dumps(request.data)
        logger.info("=================PAYLOAD===============================")
        logger.info(payload)
        logger.info("====================================================")

        response = requests.post(URL, data=payload, headers=headers)
        logger.info("====================================================")
        logger.info(URL)
        logger.info("====================================================")
        logger.info(response.elapsed.total_seconds())
        logger.info(response.status_code)
        logger.info(response.headers)
        logger.info("====================================================")

        add_audit_to_database.delay(
            http_method=HTTP_METHOD,
            request_url=response.url,
            response_time=response.elapsed.total_seconds(),
            response_code=response.status_code,
            integrating_app_id=obj_integration_app.pk,
        )
        if not response.ok:
            logger.error("POST request failed")
            return Response({"message": response.text}, status=response.status_code)

        if JSON_CONTENT_TYPE not in response.headers.get("Content-Type"):
            return Response(
                {
                    "message": "The response content type {} is not supported.".format(
                        response.headers.get("Content-Type")
                    )
                },
                status=403,
            )
        json_response = response.json()
        if not json_response.get("data", None):
            json_response = {"data": json_response}
        serializer = IntelliRouteSerializer(json_response)
        return Response(serializer.data, status=response.status_code)


class IntelliRouteDetail(APIView):
    """
    Routes a GET single or PUT or DELETE requests
    """

    def get(self, request, pk, format=None):
        ALIAS = "alias"
        RESOURCE = "resource"
        HTTP_METHOD = "GET"
        headers = {"Content-Type": JSON_CONTENT_TYPE}

        logger.info("====================================================")
        alias = request.GET.get(ALIAS)
        resource = request.GET.get(RESOURCE)
        query_string = request.META.get("QUERY_STRING")
        logger.info(alias)
        logger.info(resource)
        logger.info(query_string)

        obj_integration_app = get_object_or_404(IntegratingApp, alias=alias)
        URL = obj_integration_app.base_url

        if resource:
            URL = URL + resource + "/"
        URL = URL + pk + "/"
        if query_string:
            URL = URL + "?" + query_string

        response = requests.get(URL, headers=headers)
        logger.info("====================================================")
        logger.info(URL)
        logger.info("====================================================")
        logger.info(response.elapsed.total_seconds())
        logger.info(response.status_code)
        logger.info(response.headers)
        logger.info("====================================================")

        add_audit_to_database.delay(
            http_method=HTTP_METHOD,
            request_url=response.url,
            response_time=response.elapsed.total_seconds(),
            response_code=response.status_code,
            integrating_app_id=obj_integration_app.pk,
        )
        if not response.ok:
            logger.error("GET request failed")
            return Response({"message": "Request failed"}, status=response.status_code)

        if JSON_CONTENT_TYPE not in response.headers.get("Content-Type"):
            return Response(
                {
                    "message": "The response content type {} is not supported.".format(
                        response.headers.get("Content-Type")
                    )
                },
                status=403,
            )

        json_response = response.json()
        if not json_response.get("data", None):
            json_response = {"data": json_response}
        serializer = IntelliRouteSerializer(json_response)
        return Response(serializer.data, status=response.status_code)

    def put(self, request, pk, format=None):
        ALIAS = "alias"
        RESOURCE = "resource"
        HTTP_METHOD = "PUT"
        headers = {"Content-Type": JSON_CONTENT_TYPE}

        logger.info("====================================================")
        alias = request.GET.get(ALIAS)
        resource = request.GET.get(RESOURCE)
        query_string = request.META.get("QUERY_STRING")
        logger.info(alias)
        logger.info(resource)
        logger.info(query_string)

        obj_integration_app = get_object_or_404(IntegratingApp, alias=alias)
        URL = obj_integration_app.base_url

        if resource:
            URL = URL + resource + "/"
        URL = URL + pk + "/"
        if query_string:
            URL = URL + "?" + query_string

        payload = json.dumps(request.data)
        logger.info("=================PAYLOAD===============================")
        logger.info(payload)
        logger.info("====================================================")

        response = requests.put(URL, data=payload, headers=headers)
        logger.info("====================================================")
        logger.info(URL)
        logger.info("====================================================")
        logger.info(response.elapsed.total_seconds())
        logger.info(response.status_code)
        logger.info(response.headers)
        logger.info("====================================================")

        add_audit_to_database.delay(
            http_method=HTTP_METHOD,
            request_url=response.url,
            response_time=response.elapsed.total_seconds(),
            response_code=response.status_code,
            integrating_app_id=obj_integration_app.pk,
        )
        if not response.ok:
            logger.error("PUT request failed")
            return Response({"message": "Request failed"}, status=response.status_code)

        json_response = response.json()
        if not json_response.get("data", None):
            json_response = {"data": json_response}
        serializer = IntelliRouteSerializer(json_response)
        return Response(serializer.data, status=response.status_code)

    def delete(self, request, pk, format=None):
        ALIAS = "alias"
        RESOURCE = "resource"
        HTTP_METHOD = "DELETE"
        headers = {"Content-Type": JSON_CONTENT_TYPE}

        logger.info("====================================================")
        alias = request.GET.get(ALIAS)
        resource = request.GET.get(RESOURCE)
        query_string = request.META.get("QUERY_STRING")
        logger.info(alias)
        logger.info(resource)
        logger.info(query_string)

        obj_integration_app = get_object_or_404(IntegratingApp, alias=alias)
        URL = obj_integration_app.base_url

        if resource:
            URL = URL + resource + "/"
        URL = URL + pk + "/"
        if query_string:
            URL = URL + "?" + query_string

        response = requests.delete(URL, headers=headers)
        logger.info("====================================================")
        logger.info(URL)
        logger.info("====================================================")
        logger.info(response.elapsed.total_seconds())
        logger.info(response.status_code)
        logger.info(response.headers)
        logger.info("====================================================")

        add_audit_to_database.delay(
            http_method=HTTP_METHOD,
            request_url=response.url,
            response_time=response.elapsed.total_seconds(),
            response_code=response.status_code,
            integrating_app_id=obj_integration_app.pk,
        )
        if not response.ok:
            logger.error("DELETE request failed")
            return Response({"message": "Request failed"}, status=response.status_code)

        if JSON_CONTENT_TYPE not in response.headers.get("Content-Type"):
            return Response(
                {
                    "message": "The response content type {} is not supported.".format(
                        response.headers.get("Content-Type")
                    )
                },
                status=403,
            )

        json_response = response.json()
        if not json_response.get("data", None):
            json_response = {"data": json_response}
        serializer = IntelliRouteSerializer(json_response)
        return Response(serializer.data, status=response.status_code)
