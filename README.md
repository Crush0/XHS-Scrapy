# XHS-Scrapy-JS
在浏览器端运行的小红书爬虫，可爬取无水印图片和视频

## 由于XHS限制，目前仅可爬取前40个

# 使用方法
- 1.打开你想要爬取的博客的个人主页，F12打开开发者工具
- 2.将scrapy.js中的内容剪切到控制台中运行，下载完成后将自动打包zip文件下载

# Tips
- 1.你可以在运行代码之前选择爬取类型，只需要修改代码首部的`FETCH_VIDEO`或`FETCH_IMAGE`，默认只爬取图片
- 2.你可以随时在爬取过程中在控制台中输入`zipSave()`来立即下载已经爬取完毕的部分
