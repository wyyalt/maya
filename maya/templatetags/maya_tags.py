from django.template import Library
from types import FunctionType

register = Library()

def format_data_body(data_list,list_display,maya_admin):
    """
    格式化数据行
    :param data_list:
    :param list_display:
    :param maya_admin:
    :return:
    """
    for row in data_list:
        # yield [ getattr(row,col_name) for col_name in list_display ]
        yield [ col_name(maya_admin,row) if isinstance(col_name,FunctionType) else getattr(row,col_name) for col_name in list_display ]

def format_data_head(list_display):
    ret = []
    for col_name in list_display:
        if isinstance(col_name,FunctionType):
            ret.append(col_name.__name__.title())
        else:
            ret.append(col_name.title())

    return ret



@register.inclusion_tag('for_change_list.html')
def change_list(data_list,list_display,maya_admin):
    return {'result':format_data_body(data_list,list_display,maya_admin),'head':format_data_head(list_display)}
