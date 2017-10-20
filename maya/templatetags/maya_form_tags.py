from django.template import Library
from django.forms.models import ModelChoiceField
from django.urls import reverse
from maya.service import admin

register = Library()

def get_add_edit_form(form):
    for item in form:
        form_dict = {'is_popup':False,'item':None,'target_url':None}
        if isinstance(item.field,ModelChoiceField) and item.field.queryset.model in admin.site._registry:
            form_dict['is_popup'] = True
            form_dict['item'] = item

            target_app_label = item.field.queryset.model._meta.app_label
            target_model_name = item.field.queryset.model._meta.model_name

            target_url = "{0}?popup={1}".format(reverse("{0}:{1}_{2}_add".format(admin.site.namespace,target_app_label,target_model_name)),item.auto_id)
            form_dict['target_url'] = target_url

        else:
            form_dict['item'] = item

        yield form_dict

@register.inclusion_tag('show_add_edit_form.html')
def show_add_edit_form(form):
    return {'form_list':get_add_edit_form(form)}




