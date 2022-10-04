from django import forms
from django.shortcuts import render, redirect, HttpResponse
from UMS import models
from UMS.utils.encrypt import md5


class AdminForm(forms.Form):
    username = forms.CharField(
        label="用户名",
        widget=forms.TextInput(
            attrs={"class": "form-control",
                   "placeholder": "用户名",
                   }
        ),
        required= True,
    )
    password = forms.CharField(
        label="密码",
        widget=forms.PasswordInput(
            attrs={"class": "form-control",
                   "placeholder": "密码",
                   },
            render_value= True,
        ),
        required=True,
    )
    def clean_password(self):
        pwd = self.cleaned_data.get("password")
        return md5(pwd)


def account_login(request):
    if request.method == "GET":
        form = AdminForm()
        return render(request, 'account_login.html', {"form": form})
    form = AdminForm(data=request.POST)
    if form.is_valid():
        admin_obj = models.Admin.objects.filter(**form.cleaned_data).first()
        if not admin_obj:
            form.add_error("password", "用户或密码错误")
            return render(request, 'account_login.html', {"form": form})
        request.session['info'] = {"id": admin_obj.id, "username": admin_obj.username}
        return redirect('/admin/list/')
    return render(request, 'account_login.html', {"form": form})


def account_logout(request):
    request.session.clear()
    return redirect('/login/')
