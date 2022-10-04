from django.utils.deprecation import MiddlewareMixin
from django.shortcuts import render, redirect, HttpResponse

class AuthMiddleWare(MiddlewareMixin):
    """中间件"""
    def process_request(self, request):
        if request.path_info == "/login/":
            return

        info_dict = request.session.get("info")
        if info_dict:
            return
        return redirect('/login/')
