from types import FunctionType
from django.utils.safestring import mark_safe
from copy import deepcopy
class SearchOption(object):
    def __init__(self, field_or_func, is_multi,text_func_name=None,value_func_name=None):
        self.field_or_func = field_or_func
        self.is_multi = is_multi
        self.text_func_name = text_func_name
        self.value_func_name = value_func_name

    @property
    def is_func(self):
        if isinstance(self.field_or_func, FunctionType):
            return True

    @property
    def name(self):
        if self.is_func:
            return self.field_or_func.__name__
        else:
            return self.field_or_func

class FilterList(object):
    def __init__(self,option,queryset,request):
        self.option = option
        self.queryset = queryset
        self.param_dict = deepcopy(request.GET)
        self.param_dict._mutable = True
        self.path_info = request.path_info

    def __iter__(self):
        #生成all_url
        yield mark_safe("<div class='filter_all'>")
        if self.option.name in self.param_dict:
            #pop当前option
            pop_val = self.param_dict.pop(self.option.name)
            all_url = "{0}?{1}".format(self.path_info,self.param_dict.urlencode())

            #保留原搜索条件
            self.param_dict.setlist(self.option.name,pop_val)
            yield mark_safe("<a href='{0}'>全部</a>".format(all_url))
        else:
            all_url = "{0}?{1}".format(self.path_info, self.param_dict.urlencode())
            yield mark_safe("<a class='active' href='{0}'>全部</a>".format(all_url))

        yield mark_safe("</div><div class='filter_list'>")

        from django.http.request import QueryDict

        #list_url
        for row in self.queryset:
            param_dict = deepcopy(self.param_dict)
            val = getattr(row,self.option.value_func_name)() if self.option.value_func_name else row.pk
            val = str(val)
            content = getattr(row,self.option.text_func_name)() if self.option.text_func_name else str(row)

            active = False
            if self.option.is_multi:
                value_list = param_dict.getlist(self.option.name)

                if val in value_list:
                    value_list.remove(val)
                    param_dict.setlist(self.option.name,value_list)
                    active = True
                else:
                    param_dict.appendlist(self.option.name, val)
            else:
                option = param_dict.getlist(self.option.name)
                if val in option:
                    active = True
                param_dict[self.option.name] = val

            list_url = "{0}?{1}".format(self.path_info,param_dict.urlencode())
            if active:
                tpl = "<a class='active' href='{0}'>{1}</a>".format(list_url,content)
            else:
                tpl = "<a href='{0}'>{1}</a>".format(list_url, content)
            yield mark_safe(tpl)
        yield mark_safe("</div>")