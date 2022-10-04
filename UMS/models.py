from django.db import models

# Create your models here.
class Department(models.Model):
    """部门表"""
    title = models.CharField(verbose_name="标题", max_length=32)
    def __str__(self):
        return self.title

class UserInfo(models.Model):
    """员工表"""
    name = models.CharField(verbose_name="姓名", max_length=16)
    password = models.CharField(verbose_name="密码", max_length=64)
    age = models.IntegerField(verbose_name="年龄")
    account = models.DecimalField(verbose_name="账户余额", max_digits=10, decimal_places=2, default=0)
    # create_time = models.DateTimeField(verbose_name="创建时间")
    create_time = models.DateField(verbose_name="创建时间")
    #构建外键, 可以为空时null=True, blank=True
    depart = models.ForeignKey(verbose_name="所属部门", to="Department", to_field="id", null=True, blank=True, on_delete=models.SET_NULL)
    gender_choices=(
        (1,"男"),
        (2,"女"),
    )
    gender = models.SmallIntegerField(verbose_name="性别", choices=gender_choices)

class PrettyNum(models.Model):
    """靓号表"""
    mobile = models.CharField(verbose_name="电话号码", max_length=11)
    price = models.IntegerField(verbose_name="价格")
    level_choices=(
        (1, "超级靓"),
        (2, "特别靓"),
        (3, "一般靓"),
    )
    level = models.SmallIntegerField(verbose_name="靓号等级", choices=level_choices, default=1)
    status_choices=(
        (1, "未占用"),
        (2, "已占用"),
    )
    status = models.SmallIntegerField(verbose_name="占用状态", choices=status_choices, default=1)

class Admin(models.Model):
    """员工表"""
    username = models.CharField(verbose_name="用户名", max_length=32)
    password = models.CharField(verbose_name="密码", max_length=64)
    def __str__(self):
        return self.username

class Order(models.Model):
    """订单"""
    oid = models.CharField(verbose_name="订单号", max_length=32)
    title = models.CharField(verbose_name="商品名称", max_length=32)
    price = models.IntegerField(verbose_name="价格")
    status_choice = (
        (1, "待支付"),
        (2, "已支付"),
    )
    status = models.SmallIntegerField(verbose_name="状态", choices=status_choice, default=1)
    admin = models.ForeignKey(verbose_name="负责人", to="Admin", on_delete=models.CASCADE)