# ==============================================================================
# 注意：本脚本包含两种图片转文字（OCR）的实现方式：
# 1. 在线识别（基于百度云 AipOcr）
# 2. 离线识别（基于 pytesseract 和 Pillow）
#
# 运行本脚本前，需要安装相应的依赖（本环境未安装，仅提供代码实现）：
# pip install baidu-aip pytesseract Pillow
# 且离线识别需要系统安装 Tesseract-OCR 引擎。
# ==============================================================================

import os

# ------------------------------------------------------------------------------
# 方式一：在线文字识别（以百度云 AI 为例）
# ------------------------------------------------------------------------------
def online_ocr_baidu(image_path):
    """
    使用百度云 AipOcr 进行在线文字识别
    """
    try:
        from aip import AipOcr
    except ImportError:
        print("未安装 baidu-aip 库。请执行: pip install baidu-aip")
        return

    # ================= 配置区域 =================
    # 你的 APPID AK SK (需要去百度云控制台申请)
    APP_ID = '你的 App ID'
    API_KEY = '你的 Api Key'
    SECRET_KEY = '你的 Secret Key'
    # ============================================

    if APP_ID == '你的 App ID':
        print("请先在代码中配置百度云的 APP_ID, API_KEY, SECRET_KEY")
        return

    print(f"正在使用百度云在线识别图片: {image_path} ...")
    client = AipOcr(APP_ID, API_KEY, SECRET_KEY)

    # 读取图片
    def get_file_content(filePath):
        with open(filePath, 'rb') as fp:
            return fp.read()

    if not os.path.exists(image_path):
        print(f"图片不存在: {image_path}")
        return

    image_data = get_file_content(image_path)

    # 调用通用文字识别, 图片参数为本地图片
    result = client.basicGeneral(image_data)
    
    # 识别成功后的文字处理工作 (从字典转换为列表并提取文本)
    if 'words_result' in result:
        info = []
        for item in result['words_result']:
            info.append(item['words'])
        
        print("\n--- 在线识别结果 ---")
        for line in info:
            print(line)
        print("--------------------\n")
    else:
        print("在线识别失败或未返回文字结果:", result)


# ------------------------------------------------------------------------------
# 方式二：离线文字识别（基于 Tesseract）
# ------------------------------------------------------------------------------
def offline_ocr_tesseract(image_path):
    """
    使用 pytesseract 进行离线文字识别，并包含提高准确率的图片预处理步骤
    """
    try:
        import pytesseract
        from PIL import Image
    except ImportError:
        print("未安装 pytesseract 或 Pillow 库。请执行: pip install pytesseract Pillow")
        return

    if not os.path.exists(image_path):
        print(f"图片不存在: {image_path}")
        return

    print(f"正在使用 Tesseract 离线识别图片: {image_path} ...")
    
    # 打开图片
    image = Image.open(image_path)

    # 1. 预处理：转为灰度图片
    imgry = image.convert('L')

    # 2. 预处理：二值化，采用阈值分割算法
    # threshold为分割点, 根据图片质量调节 (0-255)
    threshold = 150
    table = []
    for j in range(256):
        if j < threshold:
            table.append(0)
        else:
            table.append(1)

    # point() 函数用于对图像的每个像素点进行操作，'1' 表示二值图像
    temp = imgry.point(table, '1')

    # 3. OCR识别
    # lang="chi_sim+eng" 指定中文简体和英文
    # config='--psm 6' 表示按行识别（Assume a single uniform block of text），有助于提升识别准确率
    try:
        text = pytesseract.image_to_string(temp, lang="chi_sim+eng", config='--psm 6')
        
        print("\n--- 离线识别结果 ---")
        print(text)
        print("--------------------\n")
    except Exception as e:
        print(f"离线识别失败 (请确保系统已安装 Tesseract-OCR 引擎): {e}")


if __name__ == "__main__":
    # 测试用的图片路径
    TEST_IMAGE_PATH = "example.png"
    
    # 创建一个空的测试图片文件，防止直接报错找不到文件
    if not os.path.exists(TEST_IMAGE_PATH):
        with open(TEST_IMAGE_PATH, 'w') as f:
            f.write("")
            
    print("=== 图片转文字自动化脚本 ===")
    
    # 测试在线识别
    online_ocr_baidu(TEST_IMAGE_PATH)
    
    # 测试离线识别
    offline_ocr_tesseract(TEST_IMAGE_PATH)
    
    # 清理测试文件
    if os.path.exists(TEST_IMAGE_PATH) and os.path.getsize(TEST_IMAGE_PATH) == 0:
        os.remove(TEST_IMAGE_PATH)
