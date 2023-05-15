### dash搭建多页面示例
```
dash render web applications as a 'single-page app'. 
当使用dcc.link的时候，当导航到不同的页面时，app并不会完全的重载， 这种方式使dash
运行的非常快。
```

dcc.Location 
dcc.Link  

### 创建多页面的步骤
1 每个页面需要单独的.py文件，并且把他们放在/pages目录下面 
2 对于每个页面的.py文件，需要进行以下操作：

    - 2.1 dash.register_page(__name__)，告诉dash这个你app中的一个页面
    - 2.2 定义layout变量 
3 主文件app.py 

    3.1 当运行app时，记得使用app = Dash(__name__, use_pages=True)
    3.2 Add dash.page_container in your app layout where you want the page content to be displayed when a user visits one of the app's page paths.