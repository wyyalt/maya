from django.shortcuts import render,HttpResponse
from django.urls import reverse

# Create your views here.


def test(request):
    #反向生成URL
    url = reverse('maya:app01_userinfo_add')
    print(url)
    return HttpResponse("...")
