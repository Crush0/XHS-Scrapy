# XHS-Scrapy
# 小红书爬虫

## 使用方法

### 1.安装依赖
```bash
  pip install PyExecJS
  pip install requests
```

### 2.从网页中获得你的Cookie


![获得COOKIE](https://user-images.githubusercontent.com/54226076/230703848-480b214e-6f59-4caa-80c2-9c0e3af0d4e9.png)

从界面上获得地址栏中的要爬取的用户编号，然后获得你的cookie

### 3.运行程序

```bash
  python main.py --user_id=[要爬取的用户ID] "--cookie=[你的Cookie]"
```

默认情况下，保存的图片和视频将会在程序目录下的output文件夹中。

### 4.额外参数

除了user_id和cookie，你也可以指定是否抓取视频和图片，和指定输出路径，你可以增加如下参数
默认视频和图片都抓取

```bash
  python main.py --user_id=[要爬取的用户ID] "--cookie=[你的Cookie]" --output=D:\output --fetch_image=False
```
