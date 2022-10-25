from rest_framework.renderers import JSONRenderer
from django.conf import settings as app_settings
STATUS = app_settings.STATUS_CODES


class CustomRenderer(JSONRenderer):
    def render(self, data, accepted_media_type=None, renderer_context=None):
        status_code = renderer_context["response"].status_code
        response = {
            "success": True,
            'status': STATUS.get('success', ''),
            "data": data,
            "detail": "Data Retrieved successfully"}
        if not str(status_code).startswith("2"):
            response["status"] = "error"
            response["data"] = None
            try:
                response["message"] = data["detail"]
            except KeyError:
                response["data"] = data
        return super(CustomRenderer, self).render(response, accepted_media_type, renderer_context)

# you just need to put renderer_class = (CustomRender)