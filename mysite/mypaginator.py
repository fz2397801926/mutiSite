from django.core.paginator import Paginator,EmptyPage,PageNotAnInteger

# 扩展paginator
class MyPaginator(Paginator):
    def __init__(self,currentPage,maxShowedPage,*args,**kwargs):
        # 当前页
        self.currentPage = int(currentPage)
        # 最大显示页数
        self.maxShowedPage = int(maxShowedPage)

        super(MyPaginator,self).__init__(*args,**kwargs)

    # 显示的页数范围
    def showPageRange(self):
        halfPart = int(self.maxShowedPage / 2)
        pageRange = range(self.currentPage-halfPart, self.currentPage+halfPart)
        # 总页数少
        if self.num_pages  <= self.maxShowedPage:
            pageRange = range(1, self.num_pages+1)
        # 总页数多
        else:
            # 开始几页
            if self.currentPage <= halfPart:
                pageRange = range(1, self.maxShowedPage+1)
            # 最后几页
            elif self.currentPage > (self.num_pages - halfPart):
                pageRange = range(self.currentPage-halfPart, self.num_pages+1)
        return pageRange
