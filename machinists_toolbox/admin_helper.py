""" Django admin helper functions """
from django.contrib.contenttypes.models import ContentType
from django.urls import reverse
from django.utils.html import format_html
from django.utils.http import urlencode


def changelist_url(model_class) -> str:
    """ Return admin changelist url for the given model class """
    obj_content_type = ContentType.objects.get_for_model(model_class)
    return reverse(
        f"admin:{obj_content_type.app_label}_{obj_content_type.model}_changelist"
    )


def changelist_link(model_class, link_title: str, filter_dict: dict[str, str] = None):
    url = changelist_url(model_class)
    if filter_dict:
        url = url + "?" + urlencode(filter_dict)
    return format_html('<a href="{}">{}</a>', url, link_title)