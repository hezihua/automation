import os
from win32com import client
from PyPDF2 import PdfReader, PdfWriter

def word2pdf(filepath, wordname, pdfname):
    """将Word文档转换为PDF"""
    worddir = filepath
    # 指定Word类型
    word = client.DispatchEx("Word.Application")
    try:
        # 使用Word软件打开文件
        file = word.Documents.Open(rf"{worddir}\{wordname}", ReadOnly=1)
        # 文件另存为当前目录下的pdf文件
        file.ExportAsFixedFormat(rf"{worddir}\{pdfname}", FileFormat=17, Item=7, CreateBookmarks=0)
        file.Close()
    except Exception as e:
        print(f"Word转换失败: {e}")
    finally:
        # 结束word应用程序进程   
        word.Quit()

def excel2pdf(filepath, excelname, pdfname):
    """将Excel表格转换为PDF"""
    exceldir = filepath
    # 指定Excel类型
    excel = client.DispatchEx("Excel.Application")
    try:
        # 使用Excel软件打开文件
        file = excel.Workbooks.Open(rf"{exceldir}\{excelname}", False)
        # 文件另存为当前目录下的pdf文件
        file.ExportAsFixedFormat(0, rf"{exceldir}\{pdfname}")
        file.Close()
    except Exception as e:
        print(f"Excel转换失败: {e}")
    finally:
        # 结束excel应用程序进程   
        excel.Quit()

def ppt2pdf(filepath, pptname, pdfname):
    """将PowerPoint幻灯片转换为PDF"""
    pptdir = filepath
    # 指定PPT类型
    ppt = client.DispatchEx("PowerPoint.Application")
    try:
        # 使用ppt软件打开文件
        file = ppt.Presentations.Open(rf"{pptdir}\{pptname}", False)
        # 文件另存为当前目录下的pdf文件
        file.ExportAsFixedFormat(rf"{pptdir}\{pdfname}")
        file.Close()
    except Exception as e:
        print(f"PPT转换失败: {e}")
    finally:
        # 结束ppt应用程序进程
        ppt.Quit()

def add_watermark(pdf_without_watermark, watermark_file, pdf_with_watermark):
    """为PDF文件批量添加水印"""
    # 准备合并后的文件对象
    pdf_writer = PdfWriter()

    try:
        # 读取水印文件和目标PDF
        watermark_reader = PdfReader(watermark_file)
        watermark_page = watermark_reader.pages[0]

        target_reader = PdfReader(pdf_without_watermark)

        # 遍历目标PDF的每一页，合并水印
        for page in target_reader.pages:
            page.merge_page(watermark_page)
            pdf_writer.add_page(page)

        # 写入新的PDF文件
        with open(pdf_with_watermark, "wb") as f:
            pdf_writer.write(f)
            
        print(f"成功添加水印: {pdf_with_watermark}")
    except Exception as e:
        print(f"添加水印失败: {e}")

def batch_process(folder_path, watermark_pdf_path):
    """批量处理文件夹中的所有Office文件：转PDF并加水印"""
    if not os.path.exists(folder_path):
        print("指定的文件夹不存在！")
        return

    for filename in os.listdir(folder_path):
        file_path = os.path.join(folder_path, filename)
        if not os.path.isfile(file_path) or filename.startswith('~$'):
            continue # 跳过文件夹和Office临时文件

        name, ext = os.path.splitext(filename)
        ext = ext.lower()
        
        pdf_name = f"{name}.pdf"
        watermarked_pdf_name = f"{name}_watermarked.pdf"
        
        pdf_full_path = os.path.join(folder_path, pdf_name)
        watermarked_full_path = os.path.join(folder_path, watermarked_pdf_name)

        # 1. 格式转换
        if ext in ['.doc', '.docx']:
            print(f"正在转换 Word: {filename} ...")
            word2pdf(folder_path, filename, pdf_name)
        elif ext in ['.xls', '.xlsx']:
            print(f"正在转换 Excel: {filename} ...")
            excel2pdf(folder_path, filename, pdf_name)
        elif ext in ['.ppt', '.pptx']:
            print(f"正在转换 PPT: {filename} ...")
            ppt2pdf(folder_path, filename, pdf_name)
        else:
            continue # 非Office文件跳过

        # 2. 添加水印
        if os.path.exists(pdf_full_path) and os.path.exists(watermark_pdf_path):
            print(f"正在为 {pdf_name} 添加水印 ...")
            add_watermark(pdf_full_path, watermark_pdf_path, watermarked_full_path)

if __name__ == "__main__":
    # ================= 配置区域 =================
    # 1. 需要处理的Office文件所在的文件夹绝对路径 (请使用双斜杠或前缀r)
    TARGET_FOLDER = r"C:\data" 
    
    # 2. 提前准备好的仅包含水印的PDF文件路径
    WATERMARK_FILE = r"C:\data\watermark.pdf" 
    # ============================================
    
    batch_process(TARGET_FOLDER, WATERMARK_FILE)
    print("全部处理完成！")
