from django.shortcuts import render, redirect
from UMS.utils.pagination import Pagination
from UMS.utils.form import NumModelform
from UMS import models

def num_list(request):

    #搜索框
    date_dict = {}
    search_data = request.GET.get("q","")
    if search_data:
        date_dict["mobile__contains"] = search_data
    queryset = models.PrettyNum.objects.filter(**date_dict).order_by("level")


    page_obj = Pagination(request, queryset)

    context={
        "search_data": search_data,
        "queryset": page_obj.page_queryset,
        "page_string": page_obj.html(),
    }
    return render(request, "prettynum_list.html", context)

def num_add(request):
    if request.method == "GET":
        form = NumModelform()
        context ={
            "form": form
        }
        return render(request, "prettynum_add.html", context)
    form = NumModelform(data=request.POST)
    if form.is_valid():
        form.save()
        return redirect('/num/list/')
    return render(request, "prettynum_add.html", {"form":form})

def num_edit(request, nid):
    row_object = models.PrettyNum.objects.filter(id=nid).first()
    if request.method == "GET":
        form = NumModelform(instance=row_object)
        return render(request, 'prettynum_edit.html', {"form":form})
    form = NumModelform(data=request.POST, instance=row_object)
    if form.is_valid():
        form.save()
        return redirect('/num/list/')
    return render(request, 'prettynum_edit.html', {"form":form})

def num_delete(request, nid):
    models.PrettyNum.objects.filter(id=nid).delete()
    return redirect('/num/list/')