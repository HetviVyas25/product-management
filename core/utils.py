
from rest_framework.response import Response

from django.core.paginator import Paginator


def create_response(data, code, message=None, extra={}):
    # extra["media_url"] = dj_settings.MEDIA_URL
    if not message:
        if code == 400:
            message = "Bad request"

        if code == 200:
            message = "Success"

    return Response(
        {"data": data, "message": message, "code": code, "extra": extra}, code
    )


def pagination_on_queryset(queryset, page, per_page_items):
    if not per_page_items:
        per_page_items = 1

    p = Paginator(queryset, per_page_items)

    try:
        page_instance = p.page(page)
        print("page_instance===>", page_instance)
    except Exception as e:  # noqa
        print("error is ", e)
        return {
            "page_count": p.num_pages,
            "data":[]
            }

    return {
        "data": page_instance.object_list,
        "page_count": p.num_pages,
        "current_page": page,
        "next_page":int(page)+1
    }
