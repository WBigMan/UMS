from django.shortcuts import render,redirect

def chart_list(request):
    return render(request, "chart_list.html")