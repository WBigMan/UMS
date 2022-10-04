from django.shortcuts import render, redirect
from UMS.models import Department


def depart_list(request):
    """部门列表"""
    de_list = Department.objects.all()
    return render(request, "depart_list.html", {"de_list":de_list})

def depart_add(request):
    """添加部门"""
    if request.method == "POST":
        title = request.POST.get("title")
        Department.objects.create(title=title)
        return redirect("/depart/list/")
    return render(request, "depart_add.html")

def depart_delete(request):
    nid=request.GET.get("nid")
    Department.objects.filter(id=nid).delete()
    return redirect("/depart/list/")

def depart_edit(request,nid):
    if request.method == "GET":
        e_depart = Department.objects.filter(id=nid).first()
        return render(request, "depart_edit.html", {"e_depart":e_depart})
    e_depart = request.POST.get("title")
    Department.objects.filter(id=nid).update(title=e_depart)
    return redirect("/depart/list/")

from openpyxl import load_workbook
def depart_multi(request):
    file_object = request.FILES.get("exc")
    wb = load_workbook(file_object)
    sheet = wb.worksheets[0]

