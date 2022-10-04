from django.shortcuts import render, redirect
from UMS.utils.form import OrderModelform
from django.views.decorators.csrf import csrf_exempt
from django.http import JsonResponse
import random
from datetime import datetime
from UMS.models import Order
from UMS.utils.pagination import Pagination


def order_list(request):
    queryset = Order.objects.all().order_by("-id")
    page_obj = Pagination(request, queryset)
    form = OrderModelform()
    context = {
        "form": form,
        "queryset": page_obj.page_queryset,
        "page_string": page_obj.html(),
    }
    return render(request, "order_list.html", context)


@csrf_exempt
def order_add(request):
    """新建订单"""
    form = OrderModelform(data=request.POST)
    if form.is_valid():
        form.instance.oid = datetime.now().strftime("%Y%m%d%H%M%S") + str(random.randint(1000, 9999))
        form.instance.admin_id = request.session["info"]["id"]
        form.save()
        return JsonResponse({"status": True})
    return JsonResponse({"status": False, "error": form.errors})


def order_delete(request):
    uid = request.GET.get("uid")
    exist = Order.objects.filter(id=uid).exists()
    if not exist:
        return JsonResponse({"status": False, "error": "要删除的数据不存在，删除失败"})
    Order.objects.filter(id=uid).delete()
    return JsonResponse({"status": True})


def order_detail(request):
    uid = request.GET.get("uid")
    row_dict = Order.objects.filter(id=uid).values("title", "price", "status").first()
    if not row_dict:
        return JsonResponse({"status": False, "error": "编辑内容不存在，请刷新后重新编辑。"})
    result = {
        "status": True,
        "data": row_dict,
    }
    return JsonResponse(result)



@csrf_exempt
def order_edit(request):
    uid = request.GET.get("uid")
    row_obj = Order.objects.filter(id=uid).first()
    if not row_obj:
        return JsonResponse({"status": False, "tip": "编辑数据不存在"})
    form = OrderModelform(data=request.POST, instance=row_obj)
    if form.is_valid():
        form.save()
        return JsonResponse({"status": True})
    return JsonResponse({"status": False, "error": form.errors})