import os
from PIL import Image

def extract_dominant_colors(image_path, output_path, num_colors=5):
    """
    提取图片中使用最多的颜色，并将这些颜色作为色块绘制在图片左上角，然后保存。
    
    :param image_path: 原始图片路径
    :param output_path: 处理后的图片保存路径
    :param num_colors: 需要提取的颜色数量，默认为5种
    """
    try:
        # 打开图片文件
        image = Image.open(image_path)
        
        # 转换为模式P（8位深度图像，带有调色板）
        # Image.ADAPTIVE 表示自适应调色板
        image_p = image.convert("P", palette=Image.ADAPTIVE)
        
        # 获取图像的调色板（列表形式，格式为 [R, G, B, R, G, B, ...]）
        palette = image_p.getpalette()
        
        # 获取图像中使用的颜色列表，并按使用次数从大到小排序
        # getcolors() 返回格式为 [(count, index), ...]
        color_counts = sorted(image_p.getcolors(maxcolors=9999), reverse=True)
        
        # 提取使用次数最多的前 num_colors 种颜色的 RGB 值
        colors = []
        for i in range(min(num_colors, len(color_counts))):
            palette_index = color_counts[i][1]
            # 通过索引在调色板中查找真正的 RGB 颜色
            dominant_color = palette[palette_index * 3 : palette_index * 3 + 3]
            colors.append(tuple(dominant_color))
            
        print(f"[{os.path.basename(image_path)}] 提取的颜色 RGB 值: {colors}")
        
        # 将提取出的颜色作为色块绘制到原图上
        # 每个色块大小为 100x100，间隔 20 像素（总跨度 120 像素）
        for i, val in enumerate(colors):
            # paste(color, box)
            image.paste(val, (0 + i * 120, 0, 100 + i * 120, 100))
            
        # 保存并显示处理后的图片
        image.save(output_path)
        print(f"处理完成，图片已保存至: {output_path}")
        
        # 如果在支持 GUI 的环境下，可以取消注释下面这行来直接预览图片
        # image.show()
        
    except Exception as e:
        print(f"处理图片 {image_path} 时发生错误: {e}")

def batch_process_images(input_dir, output_dir):
    """
    思考题解答：批量处理文件夹中的多张图片，提取主要颜色并保存。
    """
    if not os.path.exists(input_dir):
        print(f"输入目录不存在: {input_dir}")
        return
        
    if not os.path.exists(output_dir):
        os.makedirs(output_dir)
        
    # 支持的图片格式
    valid_extensions = ('.jpg', '.jpeg', '.png', '.bmp')
    
    for filename in os.listdir(input_dir):
        if filename.lower().endswith(valid_extensions):
            input_path = os.path.join(input_dir, filename)
            
            # 构造输出文件名，例如: sunrise_colors.jpg
            name, ext = os.path.splitext(filename)
            output_filename = f"{name}_colors{ext}"
            output_path = os.path.join(output_dir, output_filename)
            
            print(f"正在处理: {filename} ...")
            extract_dominant_colors(input_path, output_path)

if __name__ == '__main__':
    # ================= 配置区域 =================
    # 测试单张图片 (请确保该路径下有一张名为 sunrise.jpg 的图片)
    # 如果没有该图片，脚本会捕获异常并打印错误信息
    TEST_IMAGE = r"sunrise.jpg"
    TEST_OUTPUT = r"sunrise_colors.jpg"
    
    # 思考题：批量处理目录配置
    INPUT_DIR = r"./images_input"
    OUTPUT_DIR = r"./images_output"
    # ============================================
    
    print("--- 1. 测试单张图片处理 ---")
    if os.path.exists(TEST_IMAGE):
        extract_dominant_colors(TEST_IMAGE, TEST_OUTPUT)
    else:
        print(f"未找到测试图片 {TEST_IMAGE}，请在当前目录放置一张图片用于测试。")
        
    print("\n--- 2. 测试批量图片处理 (思考题) ---")
    # 创建测试用的输入目录
    if not os.path.exists(INPUT_DIR):
        os.makedirs(INPUT_DIR)
        print(f"已创建输入目录 {INPUT_DIR}，请放入图片后再次运行以测试批量处理。")
    else:
        batch_process_images(INPUT_DIR, OUTPUT_DIR)
