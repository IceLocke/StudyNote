# StudyNote
## 前题
* 一个简单的记事本 Web 应用，练手项目，现在滋磁 Markdown。
* 目前写本项目花费时间：2h。

## 运行环境
1. Python 3.6.2
2. Flask 1.10.1
3. Python Markdown 模块

## 前端框架
1. Bootstrap
2. jQuery

## 发布版本
*Ver 0.0.1* 最早版本，仅仅有使用 Markdown 发布笔记功能  
*Ver 0.0.2* 使用 SQLite 存储笔记  
*Ver 0.0.3* 支持修改以及删除笔记，优化性能  

## 预计加入功能
- 笔记分类
- 表格形式整理笔记
- 用户，每个用户有单独的笔记，可以类似于 Git 的 fork 功能

## 使用方法
首先，确保你有 Python 解释器以及 Python 的包管理工具 pip。
然后在命令行输入下面的命令：
```
  git clone https://www.github.com/irook/StudyNote
  cd StudyNote
  pip install flask
  pip install markdown
  pytho StudyNote.py
```
然后在浏览器地址栏输入：
```
  localhost:3000
```
即可访问网站。  
如果需要变更端口，更改`StudyNote.py`第144行的 port=?，?为你要的端口号;)
