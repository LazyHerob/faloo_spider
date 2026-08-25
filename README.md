# 飞卢小说爬虫 (Faloo Spider)

一个基于 Python 的飞卢小说网爬虫工具，支持按书名或作者搜索小说，并自动下载所有章节内容到本地 TXT 文件。

## 功能特点

- 输入书名或作者名，自动搜索并爬取匹配的小说
- 支持多页搜索结果（默认 2 页，根据需求自行调整）
- 自动解析小说目录和正文
- 结果保存为 `小说名.txt`，便于阅读
- 可配置搜索页数、请求头、保存路径等

## 技术栈

- Python 3.8+
- requests-html
- beautifulsoup4
- lxml
- PyYAML

### 克隆项目

```bash
git clone https://github.com/LazyHerob/faloo_spider
cd faloo_spider