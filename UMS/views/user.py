from django.shortcuts import render, redirect
from UMS.models import UserInfo
from UMS.utils.pagination import Pagination
from UMS.utils.form import UserModelform

def user_list(request):
    u_list = UserInfo.objects.all()
    user_page_obj = Pagination(request, u_list)
    context={
        "u_list": user_page_obj.page_queryset,
        "page_string": user_page_obj.html()
    }

    return render(request, 'user_list.html', context)

def user_add(request):
    if request.method == "GET":
        form = UserModelform()
        context ={
            "form": form
        }
        return render(request, "user_add.html", context)
    form = UserModelform(data=request.POST)
    if form.is_valid():
        form.save()
        return redirect('/user/list/')
    return render(request, "user_add.html", {"form":form})

def user_edit(request, nid):
    row_object = UserInfo.objects.filter(id=nid).first()
    if request.method == "GET":
        form = UserModelform(instance=row_object)
        context ={
            "form": form
        }
        return render(request, "user_add.html", context)
    form = UserModelform(data=request.POST, instance=row_object)
    if form.is_valid():
        form.save()
        return redirect('/user/list/')
    return render(request, "user_edit.html", {"form":form})

def user_delete(request, nid):
    UserInfo.objects.filter(id=nid).delete()
    return redirect("/user/list/")