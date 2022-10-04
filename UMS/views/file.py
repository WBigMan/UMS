from django.shortcuts import render, redirect, HttpResponse


def file_upload(request):
    if request.method == "GET":
        return render(request, 'file_upload.html')
    file_object = request.FILES.get("avatar")

    f = open(file_object.name, mode="wb")
    for chunk in file_object.chunks():
        f.write(chunk)
    f.close()
    return HttpResponse("上传成功")
