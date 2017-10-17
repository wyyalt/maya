from django.conf.urls import url,include
from django.shortcuts import HttpResponse

class MayaAdmin(object):

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


    def changelist_view(self,request):
        info = self.model_class._meta.app_label, self.model_class._meta.model_name
        return HttpResponse('%s_%s_changelist'%info)

    def add_view(self,request):
        info = self.model_class._meta.app_label, self.model_class._meta.model_name
        return HttpResponse('%s_%s_add'%info)

    def delete_view(self,request,object_id):
        info = self.model_class._meta.app_label, self.model_class._meta.model_name
        return HttpResponse('%s_%s_delete'%info)

    def change_view(self,request,object_id):
        info = self.model_class._meta.app_label, self.model_class._meta.model_name
        return HttpResponse('%s_%s_change'%info)

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