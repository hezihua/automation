# Python 自动化办公实战脚本库

本项目包含了《Python自动化办公实战课》（尹会生）中各个核心章节的自动化脚本实现。涵盖了文件处理、数据分析、图表生成、多媒体处理、NLP情感分析等多个日常办公自动化场景。

## 📂 脚本目录与功能说明

以下是本项目中包含的脚本及其对应的课程章节和功能描述：

### 1. 文件与系统自动化
*   **`file_classifier.py`** (第20讲)：基于生产者-消费者模式，按扩展名自动将混杂的文件分类到不同的文件夹中。包含按文件大小分类的思考题实现。*(仅使用 Python 标准库)*
*   **`batch_rename.py`** (第16讲)：使用 `argparse` 接收命令行参数，批量重命名指定目录下的特定扩展名文件。
*   **`calc_sum_diff.py`** (第16讲思考题)：演示如何使用 `argparse` 处理数字类型的命令行参数。

### 2. 办公文档与邮件自动化
*   **`auto_pdf_watermark.py`** (第30讲)：调用 Windows COM 接口将 Word/Excel/PPT 批量转换为 PDF，并使用 `PyPDF2` 批量添加水印。
*   **`auto_email.py`** (第29讲)：使用 `imaplib` 自动收取邮件并根据关键字（如“故障”）进行过滤，使用 `yagmail` 自动发送邮件。
*   **`batch_print_to_pdf.vba`** (第14讲)：Excel VBA 脚本，用于一键将工作簿中的所有 Sheet 批量静默导出为 PDF 文件。

### 3. 定时任务与备份
*   **`tasks/` 目录** (第28讲)：基于 `Celery` 和 `Redis` 的分布式定时任务框架。包含按计划自动备份文件夹的作业 (`test1.py`, `test2.py`)。
*   **`auto_zip_backup.py`** (第27讲)：使用 `zipfile` 标准库进行无密码压缩备份，以及使用 `subprocess` 调用 `7z` 命令进行加密压缩备份。

### 4. 数据分析与图表可视化
*   **`pandas_pivot.py`** (第23讲)：使用 `Pandas` 自动生成数据透视表（多级索引、多聚合函数、汇总行），并导出到 Excel 的多个 Sheet 中。
*   **`seaborn_charts.py`** (第24讲)：使用 `seaborn` 绘制静态统计图表，包括鸢尾花数据集的散点图矩阵和房价走势的折线图。
*   **`pyecharts_demo.py`** (第25讲)：使用 `pyecharts` 绘制带有交互功能的全国疫情分布动态地图（HTML格式）。

### 5. 多媒体与AI处理
*   **`image_to_text.py`** (第03讲)：图片转文字（OCR）。包含基于百度云 `AipOcr` 的在线识别，以及基于 `pytesseract` 的离线识别（含灰度、二值化预处理）。
*   **`media_processor.py`** (第05讲)：使用 `subprocess` 调用外部命令行工具。调用 `ImageMagick` 进行长图拼接，调用 `FFmpeg` 进行视频拆分（切片为 TS 和 m3u8）与合并。
*   **`extract_colors.py`** (第26讲)：使用 `Pillow` (PIL) 提取图片中出现频率最高的几种主题色，并将色块绘制在原图上。
*   **`jieba_sentiment.py`** (第06讲)：NLP 文本处理。使用 `jieba` 进行中文分词与词性过滤，使用 `snownlp` 进行情感色彩倾向分析（正负面评价统计）。

---

## 🛠️ 环境与依赖说明

本项目中的脚本大多是独立的，您可以根据需要单独运行某个脚本。如果需要运行所有脚本，建议在虚拟环境中安装以下依赖：

### Python 第三方库
```bash
# 基础办公与数据分析
pip install pypiwin32 PyPDF2 yagmail pandas numpy openpyxl

# 图表与可视化
pip install seaborn matplotlib pyecharts

# 多媒体与AI
pip install Pillow baidu-aip pytesseract jieba snownlp

# 定时任务
pip install celery[redis] redis
```

### 外部系统依赖
部分脚本依赖于操作系统中安装的外部软件（需加入系统环境变量 `Path`）：
*   **7-Zip**: 用于 `auto_zip_backup.py` 的加密压缩。
*   **ImageMagick**: 用于 `media_processor.py` 的长图拼接。
*   **FFmpeg**: 用于 `media_processor.py` 的视频拆分与合并。
*   **Tesseract-OCR**: 用于 `image_to_text.py` 的离线文字识别。
*   **Redis**: 用于 `tasks/` 目录下的 Celery 定时任务消息队列。

---

## 🚀 运行方式

大部分脚本都可以直接通过 Python 运行，例如：
```bash
python file_classifier.py
```

带有命令行参数的脚本（如 `batch_rename.py`）：
```bash
python batch_rename.py -p /path/to/folder -e jpg
```

Celery 定时任务需要分别启动 Beat 和 Worker：
```bash
celery -A tasks beat
celery -A tasks worker --loglevel=info
```
