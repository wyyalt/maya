class PageInfo(object):
    def __init__(self,current_page,total_num,prefix_url,page_param_dict,per_page=10,show_page=10):
        """
        :param current_page: 当前页索引为类型为大于0的整数,否则会异常处理为1
        :param total_num: 数据的总数
        :param prefix_url: url前缀或者是格式为"/index/"不包含?及get参数
        :param per_page: 每页显示的内容数
        :param show_page: 分页导航显示的页数
        """
        try:
            self.current_page = int(current_page)
            if self.current_page < 0:self.current_page = 1
        except Exception:self.current_page = 1

        self.per_page=per_page
        self.page_num = self.__get_page_num(total_num,per_page)
        self.show_page = show_page
        self.total_num = total_num
        self.prefix_url = prefix_url
        self.page_param_dict = page_param_dict

    def __get_page_num(self,total_num,per_page):
        """
        :return:总页数
        """
        quotients,remainder = divmod(total_num,per_page)
        if remainder:quotients = quotients + 1
        return quotients

    @property
    def start(self):
        """
        :return: 数据开始位置
        """
        return (self.current_page-1)*self.per_page

    @property
    def end(self):
        """
        :return: 数据结束位置
        """
        return self.current_page * self.per_page

    @property
    def page_index(self):
        """
        :return: 分页导航
        """
        page_ele_list = []

        #当前页的偏移量
        offset = int(self.show_page / 2)

        #界点判断
        #总页数小于显示的页数
        if self.page_num <= self.show_page:
            first_index = 1
            last_index = self.page_num+1
        #当前页小于偏移量
        elif self.current_page <=offset:
            first_index = 1
            last_index = self.show_page + 1
        #当前页大于总页数减去偏移量
        elif self.current_page > self.page_num - offset:
            first_index = self.page_num - self.show_page + 1
            last_index = self.page_num + 1
        else:
            first_index = self.current_page - offset
            last_index = self.current_page + offset

        #上一页
        if self.current_page >1:
            self.page_param_dict['page'] = self.current_page-1
            prev_page = "<li><a href='%s?%s'>上一页</a></li>"%(self.prefix_url, self.page_param_dict.urlencode())
            page_ele_list.append(prev_page)

        #生成分页内容
        for i in range(first_index,last_index):
            self.page_param_dict['page'] = i
            if i == self.current_page:
                #当前页增加class='active'
                page_ele = "<li class='active'><a href='%s?%s'>%s</a></li>" % (self.prefix_url, self.page_param_dict.urlencode(), i)
            else:
                page_ele = "<li><a href='%s?%s'>%s</a></li>" % (self.prefix_url, self.page_param_dict.urlencode(), i)

            page_ele_list.append(page_ele)

        #下一页
        if self.current_page < self.page_num:
            self.page_param_dict['page'] = self.current_page + 1
            next_page = "<li><a href='%s?%s'>下一页</a></li>"%(self.prefix_url, self.page_param_dict.urlencode())
            page_ele_list.append(next_page)

        return "".join(page_ele_list)