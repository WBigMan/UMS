from django.shortcuts import render,redirect
from UMS import models
from UMS.utils.pagination import Pagination

def admin_list(request):
    date_dict = {}
    search_data = request.GET.get("q", "")
    if search_data:
        date_dict["mobile__contains"] = search_data
    queryset = models.Admin.objects.filter(**date_dict)

    page_obj = Pagination(request, queryset)

    context = {
        "search_data": search_data,
        "queryset": page_obj.page_queryset,
        "page_string": page_obj.html(),
    }
    return render(request, "admin_list.html", context)
from django import forms
from UMS.utils.form import AdminModelForm

def admin_add(request):
    if request.method == "GET":
        form = AdminModelForm()
    else:
        form = AdminModelForm(data=request.POST)
        if form.is_valid():
            form.save()
            return redirect('/admin/list/')
    context = {
        "title": "新建管理员",
        "form": form,
    }
    return render(request, "exchange.html", context)


def admin_edit(request, nid):

    row_obj = models.Admin.objects.filter(id=nid).first()
    if not row_obj:
        return redirect('/admin/list/')
    if request.method == "GET":
        form = AdminModelForm(instance=row_obj)
    else:
        form = AdminModelForm(data=request.POST, instance=row_obj)
        if form.is_valid():
            form.save()
            return redirect('/admin/list/')
    context = {
        "title": "管理员编辑",
        "form": form,
    }
    return render(request, 'exchange.html', context)

def admin_delete(request, nid):
    models.Admin.objects.filter(id=nid).delete()
    return redirect('/admin/list/')
