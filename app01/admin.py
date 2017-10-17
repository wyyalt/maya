
from maya.service import admin
from django.urls import reverse
from django.utils.safestring import mark_safe
from app01 import models


class UserInfoAdmin(admin.MayaAdmin):

    def edit(self,model_obj):
        """
        自定义编辑按钮
        :param model_obj:
        :return:
        """
        # reverse url
        url = reverse("{0}:{1}_{2}_change".format(
                self.site.namespace,
                self.model_class._meta.app_label,
                self.model_class._meta.model_name
            ),
            args=(model_obj.pk,)
        )

        return mark_safe("<a href='{0}'>编辑</a>".format(url))

    def select(self,model_obj):
        """
        自定义多选框
        :param model_obj:
        :return:
        """
        return mark_safe("<input type='checkbox' value='{0}'>".format(model_obj.pk))


    list_display = (select,'id','username','password',edit)
admin.site.register(models.UserInfo,UserInfoAdmin)

class UserGroupAdmin(admin.MayaAdmin):
    list_display = ('title',)
admin.site.register(models.UserGroup,UserGroupAdmin)

