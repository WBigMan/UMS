from UMS import models
from UMS.utils.bootstrapmodelform import BootStrapModelForm
from django.core.exceptions import ValidationError
from django import forms
from UMS.utils.encrypt import md5

class UserModelform(BootStrapModelForm):
    class Meta:
        model = models.UserInfo
        fields = "__all__"

class NumModelform(BootStrapModelForm):
    class Meta:
        model = models.PrettyNum
        fields = "__all__"
    """钩子判定"""
    def clean_mobile(self):
        txt_mobile = self.cleaned_data["mobile"]
        #self.instance.pk ,编辑的实例
        exists = models.PrettyNum.objects.exclude(id=self.instance.pk).filter(mobile=txt_mobile).exists()
        if exists:
            raise ValidationError("电话号码已存在")
        return txt_mobile


class AdminModelForm(BootStrapModelForm):
    confirm_password = forms.CharField(
        label= "确认密码",
        max_length= 64,
        widget=forms.PasswordInput(render_value=True)
    )
    class Meta:
        model = models.Admin
        fields = ["username", "password"]
        widgets = {
            "password": forms.PasswordInput(render_value=True),
        }
    def clean_username(self):
        username = self.cleaned_data.get("username")
        exists = models.Admin.objects.exclude(id=self.instance.pk).filter(username=username).exists()
        if exists:
            raise ValidationError("用户名已存在")
        return username

    def clean_password(self):
        pwd = self.cleaned_data.get("password")
        return md5(pwd)
    def clean_confirm_password(self):
        pwd = self.cleaned_data.get("password")
        confirm = md5(self.cleaned_data.get("confirm_password"))
        if confirm != pwd:
            raise ValidationError("密码不一致")
        return confirm


class OrderModelform(BootStrapModelForm):
    class Meta:
        model = models.Order
        exclude = ["oid", "admin"]

