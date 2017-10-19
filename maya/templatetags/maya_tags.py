from django.template import Library
from types import FunctionType

register = Library()

def format_data_body(data_list,list_display,maya_admin):
    """
    格式化数据行
    """
    for row in data_list:
        if list_display == "__all__":
            yield [str(row),]
        else:
            # yield [ getattr(row,col_name) for col_name in list_display ]
            yield [ col_name(maya_admin,model_obj=row) if isinstance(col_name,FunctionType) else getattr(row,col_name) for col_name in list_display ]

def format_data_head(list_display,maya_admin):
    if list_display == "__all__":
        yield "Objects"
    else:
        for name in list_display:
            yield name(maya_admin,is_header=True) if isinstance(name,FunctionType) else maya_admin.model_class._meta.get_field(name).verbose_name



@register.inclusion_tag('for_change_list.html')
def change_list(data_list,list_display,maya_admin):
    return {'result':format_data_body(data_list,list_display,maya_admin),'head':format_data_head(list_display,maya_admin)}


# # 横向显示
# def format_add_data_row(form,maya_admin=None,is_header=False):
#     for item in form:
#         yield maya_admin.model_class._meta.get_field(item.name).verbose_name if is_header else item
#
# # 竖向显示
# def format_add_data_col(form,maya_admin=None):
#     for item in form:
#         # yield [ maya_admin.model_class._meta.get_field(item.name).verbose_name,item,item.errors]
#         yield item
#
# @register.inclusion_tag('for_add.html')
# def add(form,maya_admin):
#
#     # return {'content':format_add_data_row(form),'head':format_add_data_row(form,maya_admin,is_header=True)}
#     return {'content_col':format_add_data_col(form,maya_admin)}

