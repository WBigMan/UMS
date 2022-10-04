"""
自定义的分页组件
在视图函数view.py中：
    1.根据自己的情况去筛选数据
        queryset = models.PrettyNum.objects.filter(**date_dict).order_by("level")
    2.实例化类,向html传参数
        page_obj = Pagination(request, queryset)
        context={
        "queryset": page_obj.page_queryset,
        "page_string": page_obj.html(),
        }
        return render(request, "prettynum_list.html", context)
在HTML中
    {* for obj in queryset *} #输出该页显示数据

    <ul class="pagination">
        {{ page_string }}
    </ul>

"""
from django.utils.safestring import mark_safe
from django.http.request import QueryDict
class Pagination(object):
    def __init__(self, request, queryset, page_param="page",page_size=15,plus=5):
        """
        :param request: 请求
        :param queryset: 需要分页的数据组
        :param page_param: 获取页码参数
        :param page_size: 每页显示的数据条数
        :param plus: 根据当前页前后显示的页码个数
        """
        #使搜索和分页可以同时有用
        import copy
        query_dict = copy.deepcopy(request.GET)
        query_dict._mutable = True
        self.query_dict = query_dict
        self.page_param = page_param

        page = request.GET.get(page_param,"1")
        if page.isdecimal():
            page = int(page)
        else:
            page = 1
        self.page = page
        self.page_size = page_size
        self.start = (page-1)*page_size
        self.end = page*page_size
        self.page_queryset = queryset[self.start: self.end]


        total_data = queryset.count()
        total_page, div = divmod(total_data, page_size)
        if div:
            total_page += 1
        self.page_totalcount = total_page
        self.plus = plus

    def html(self):
        """根据前后显示的页数plus，确定启示页"""

        if self.page_totalcount < (self.plus*2 + 1):
            start_page = 1
            end_page = self.page_totalcount
        else:
            if (self.page+self.plus) > self.page_totalcount:
                start_page = self.page_totalcount - 2*self.plus
                end_page = self.page_totalcount
            elif (self.page-self.plus) <= 1:
                start_page = 1
                end_page = self.plus*2 + 1
            else:
                start_page = self.page - self.plus
                end_page = self.page + self.plus

        #传输的HTML文件
        page_str_list = []



        #首页
        self.query_dict.setlist(self.page_param, [1])
        page_str_list.append('<li><a href="?{}">首页</a></li>'.format(self.query_dict.urlencode()))
        #上一页
        if self.page > 1:
            self.query_dict.setlist(self.page_param, [self.page - 1])
            prev = '<li><a href="?{}">上一页</a></li>'.format(self.query_dict.urlencode())
        else:
            self.query_dict.setlist(self.page_param, [1])
            prev = '<li><a href="?{}">上一页</a></li>'.format(self.query_dict.urlencode())
        page_str_list.append(prev)

        #页码
        for i in range(start_page, (end_page+1)):
            if i == self.page:
                self.query_dict.setlist(self.page_param, [i])
                ele = '<li class="active"><a href="?{}">{}</a></li>'.format(self.query_dict.urlencode(), i)
            else:
                self.query_dict.setlist(self.page_param, [i])
                ele = '<li><a href="?{}">{}</a></li>'.format(self.query_dict.urlencode(), i)
            page_str_list.append(ele)

        #下一页
        if self.page < self.page_totalcount:
            self.query_dict.setlist(self.page_param, [self.page + 1])
            prev = '<li><a href="?{}">下一页</a></li>'.format(self.query_dict.urlencode())
        else:
            self.query_dict.setlist(self.page_param, [self.page_totalcount])
            prev = '<li><a href="?{}">下一页</a></li>'.format(self.query_dict.urlencode())
        page_str_list.append(prev)

        #尾页
        self.query_dict.setlist(self.page_param, [self.page_totalcount])
        page_str_list.append('<li><a href="?{}">尾页</a></li>'.format(self.query_dict.urlencode()))
        #搜索框
        search_string = """
                    <li>
                    <form style="float: left; margin-left: 1px" class="form-inline" method="get">
                        <div class="form-group">
                            <input type="text" style="width: 100px" class="form-control" name="page" placeholder="页码">
                        </div>
                        <button type="submit" class="btn btn-default">跳转</button>
                    </form>
                </li>
        """

        page_str_list.append(search_string)

        page_string = mark_safe("".join(page_str_list))
        return page_string






