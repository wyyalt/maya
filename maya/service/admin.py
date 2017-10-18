"""
1.数据列表页面，定制显示列
    # your admin.py
    from maya.service import admin
    from [app_name] import [Model]

    示例一: 显示对象列表

        admin.site.register(Model)

    示例二: 个性化定制

        class SubClass(admin.MayaAdmin)

            def func(self,model_obj=None,is_header=False)
                if is_header:
                    return "header_name"
                else:
                    return "%s-%s"%(model_obj.username,model_obj.password)

            list_display = [func,string...]

        admin.site.register(Model,SubClass)
        PS:字段可以
            - 字符串 (数据库列名)
            - 函数

    完整示例：
        # from maya.service import admin
        # from django.urls import reverse
        # from django.utils.safestring import mark_safe
        # from app01 import models
        #
        # class UserInfoAdmin(admin.MayaAdmin):
        #
        #     def option(self,model_obj=None,is_header=False):
        #         if is_header:
        #             return "操作"
        #         else:
        #             # reverse url
        #             edit_url = reverse("{0}:{1}_{2}_change".format(
        #                     self.site.namespace,
        #                     self.model_class._meta.app_label,
        #                     self.model_class._meta.model_name
        #                 ),
        #                 args=(model_obj.pk,)
        #             )
        #             del_url = reverse("{0}:{1}_{2}_delete".format(
        #                 self.site.namespace,
        #                 self.model_class._meta.app_label,
        #                 self.model_class._meta.model_name
        #             ),
        #                 args=(model_obj.pk,)
        #             )
        #
        #             return mark_safe("<a href='{0}'>编辑</a> | <a href='{1}'>删除</a> | <a href='{1}'>详细</a>".format(edit_url,del_url))
        #
        #     def checkbox(self,model_obj=None,is_header=False):
        #         if is_header:
        #             return mark_safe(
        #                 "<input type='button' value='全选'><input type='button' value='反选'><input type='button' value='取消'>")
        #         else:
        #             return mark_safe("<input type='checkbox' value='{0}'>".format(model_obj.pk))
        #
        #
        #    list_display = (checkbox,'id','username','password',option)

"""
from django.conf.urls import url,include
from django.shortcuts import HttpResponse,render,redirect
from django.http.request import QueryDict
from django.urls import reverse

class MayaAdmin(object):

    list_display = "__all__"

    add_edit_model_from = None

    def __init__(self,model_class,site):
        self.model_class = model_class
        self.site = site

    @property
    def urls(self):
        info = self.model_class._meta.app_label,self.model_class._meta.model_name
        urlpatterns = [
            url(r'^$', self.changelist_view, name='%s_%s_changelist' % info),
            url(r'^add/$', self.add_view, name='%s_%s_add' % info),
            url(r'^(.+)/delete/$', self.delete_view, name='%s_%s_delete' % info),
            url(r'^(.+)/change/$', self.change_view, name='%s_%s_change' % info),
        ]
        return urlpatterns

    def get_add_edit_model_form(self):
        if self.add_edit_model_from:
            return self.add_edit_model_from
        else:
            from django.forms import ModelForm

            # class AddModelForm(ModelForm):
            #     class Meta:
            #         model = self.model_class
            #         fields = "__all__"

            _meta = type('Meta',(object,),{"model":self.model_class,"fields":"__all__"})
            DefaultForm = type('DefaultModelForm',(ModelForm,),{"Meta":_meta})

            return DefaultForm


    def changelist_view(self,request):
        """
        查询数据
        """

        self.request = request

        param_dict = QueryDict(mutable=True)

        #获取get参数
        if request.GET:
            param_dict['change_list_filter'] = request.GET.urlencode()

        #添加按钮URL生成
        base_add_url = reverse("{0}:{1}_{2}_add".format(self.site.namespace,self.model_class._meta.app_label,self.model_class._meta.model_name))
        add_url = "{0}?{1}".format(base_add_url,param_dict.urlencode())

        context ={
            'data_list':self.model_class.objects.all(),
            'list_display':self.list_display,
            'maya_admin':self,
            'add_url':add_url
        }

        return render(request,'change_list.html',context)

    def add_view(self,request):
        """
        添加数据
        """

        if request.method == "GET":
            AddModelForm = self.get_add_edit_model_form()()
        else:
            AddModelForm = self.get_add_edit_model_form()(data=request.POST,files=request.FILES)
            if AddModelForm.is_valid():
                AddModelForm.save()

                # 添加成功中转回list页面
                base_list_url = reverse("{0}:{1}_{2}_changelist".format(
                    self.site.namespace,
                    self.model_class._meta.app_label,
                    self.model_class._meta.model_name)
                )
                list_url = "{0}?{1}".format(base_list_url, request.GET.get('change_list_filter'))

                return redirect(list_url)

        context = {
            'form':AddModelForm,
            'maya_admin':self,
        }

        # from django.forms.boundfield import BoundField
        #
        # print(AddModelForm)
        # for item in AddModelForm:
        #     print(self.model_class._meta.get_field(item.name).verbose_name)
        #     print(type(item))
        #     print(type(item.errors))

        return render(request,'add.html',context)

    def delete_view(self,request,pk):
        """
        删除数据
        :param pk: 数据行主键id
        """
        info = self.model_class._meta.app_label, self.model_class._meta.model_name
        return HttpResponse('%s_%s_delete'%info)

    def change_view(self,request,pk):
        """
        修改数据
        :param object_id:数据行id
        """
        obj = self.model_class.objects.filter(pk=pk).first()

        if request.method == "GET":
            EditModelForm = self.get_add_edit_model_form()(instance=obj)
        else:
            EditModelForm = self.get_add_edit_model_form()(data=request.POST,files=request.FILES,instance=obj)
            if EditModelForm.is_valid():
                EditModelForm.save()

                # 添加成功中转回list页面
                base_list_url = reverse("{0}:{1}_{2}_changelist".format(
                    self.site.namespace,
                    self.model_class._meta.app_label,
                    self.model_class._meta.model_name)
                )
                list_url = "{0}?{1}".format(base_list_url, request.GET.get('change_list_filter'))

                return redirect(list_url)

        context = {
            'form':EditModelForm
        }

        return render(request,'edit.html',context)


class MayaSite(object):

    def __init__(self):
        self._registry = {}
        self.namespace = 'maya'
        self.app_name = 'maya'

    def register(self,model_class,MayaAdmin=MayaAdmin):
        self._registry[model_class] = MayaAdmin(model_class,self)

    def get_urls(self):
        urlpatterns = []

        for model_cls,maya_admin_obj in self._registry.items():
            app_label = model_cls._meta.app_label
            model_name = model_cls._meta.model_name
            urlpatterns.append(url(r'^%s/%s/'%(app_label,model_name), include(maya_admin_obj.urls)))

        return urlpatterns

    @property
    def urls(self):
        return self.get_urls(),self.app_name,self.namespace

site = MayaSite()
