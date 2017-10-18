
from maya.service import admin
from django.urls import reverse
from django.utils.safestring import mark_safe
from app01 import models
from django.http import QueryDict


class UserInfoAdmin(admin.MayaAdmin):

    def option(self,model_obj=None,is_header=False):
        """
        自定义编辑按钮
        :param model_obj:
        :return:
        """
        if is_header:
            return "操作"
        else:
            # reverse url
            base_edit_url = reverse("{0}:{1}_{2}_change".format(
                    self.site.namespace,
                    self.model_class._meta.app_label,
                    self.model_class._meta.model_name
                ),
                args=(model_obj.pk,)
            )
            base_del_url = reverse("{0}:{1}_{2}_delete".format(
                self.site.namespace,
                self.model_class._meta.app_label,
                self.model_class._meta.model_name
            ),
                args=(model_obj.pk,)
            )

            param_dict = QueryDict(mutable=True)
            param_dict['change_list_filter'] = self.request.GET.urlencode()

            edit_url = "{0}?{1}".format(base_edit_url,param_dict.urlencode())
            del_url = "{0}?{1}".format(base_del_url,param_dict.urlencode())

            option = """
            <a href='{0}'><span style="margin-right:3px" class="glyphicon glyphicon-edit" aria-hidden="true"></span>编辑</a> 
            <a href='{1}'><span style="margin-right:3px" class="glyphicon glyphicon-remove" aria-hidden="true"></span>删除</a> 
            <a href='{1}'><span style="margin-right:5px" class="glyphicon glyphicon-folder-open" aria-hidden="true"></span>查看详细</a> 
            """.format(edit_url,del_url)

            return mark_safe(option)

    def checkbox(self,model_obj=None,is_header=False):
        """
        自定义多选框
        :param model_obj:
        :return:
        """

        select = """
            <div class="btn-group first-col" role="group">
              <input type="button" class="btn btn-default btn-xs" value="全选">
              <input type="button" class="btn btn-default btn-xs" value="反选">
              <input type="button" class="btn btn-default btn-xs" value="取消">
            </div>
        """

        if is_header:
            return mark_safe(select)
        else:
            return mark_safe("<input type='checkbox' value='{0}'>".format(model_obj.pk))


    list_display = (checkbox,'id','username','password',option)
admin.site.register(models.UserInfo,UserInfoAdmin)

class UserGroupAdmin(admin.MayaAdmin):
    list_display = ('title',)
admin.site.register(models.UserGroup,UserGroupAdmin)

