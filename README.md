# 唯美女生网站爬虫<br>
## 采用requests和BeautifulSoup库
<br>
先来看看效果：
<br>
![](https://github.com/senyihui/crawl_vmgirls/raw/master/src/demo.png)

<br>
网站提供了站点地图，据此该项目分为两部分：最新文章和分类目录<br>
<br>
* download_pic():单个照片集网页的下载方法，两个download函数分别对应以上两部分（虽然除了路径内容都差不多）<br>
* classify():站点网站的解析<br>
* get_html():得到网页代码
<br>
遇到的困难在于分类目录初始页面只有八个分选图集，本来想采用requests的post的方法动态爬取（见代码注释部分），但是发现该网站是用WordPress建的，加载选项使用的是`admin-ajax-php`工具
关于这个有研究的朋友可以教教我！<br>
<br>
最后咱们的爬虫就可以开始跑了，注意设置一个`time.sleep()`哈！我们只要欣赏美，不要恶意攻击网站。<br>
<br>
欢迎交流，邮箱`senyihui123@gmail.com`
