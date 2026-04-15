import os
import shutil
from queue import Queue

# ==========================================
# 核心功能：按照扩展名对混杂的文件进行分类
# ==========================================

def make_new_dir(base_dir, type_dir_dict):
    """
    根据分类规则字典，在目标目录下建立新的分类文件夹
    """
    for folder_name in type_dir_dict.keys():
        new_dir_path = os.path.join(base_dir, folder_name)
        if not os.path.isdir(new_dir_path):
            os.makedirs(new_dir_path)
            print(f"创建分类目录: {new_dir_path}")

def write_to_q(path_to_write, q: Queue):
    """
    生产者：遍历目录，将包含文件的路径和文件列表存入队列
    """
    for full_path, dirs, files in os.walk(path_to_write):
        # 如果目录下没有文件，就跳过该目录
        if not files:
            continue
        
        # 为了避免原教程中字符串拼接解析带来的bug，这里直接将元组放入队列
        q.put((full_path, files))

def move_to_newdir(source_dir, filename, file_in_path, type_to_newpath):
    """
    将单个文件移动到对应的分类目录中
    """
    # 安全地获取文件的扩展名 (去除前面的点，并转换为小写)
    _, ext = os.path.splitext(filename)
    ext = ext.lstrip('.').lower()

    # 遍历分类规则字典，寻找匹配的扩展名
    for folder_name, ext_tuple in type_to_newpath.items():
        if ext in ext_tuple:
            oldfile = os.path.join(file_in_path, filename)
            newfile = os.path.join(source_dir, folder_name, filename)
            
            # 避免移动自己到自己，或者同名文件覆盖问题
            if oldfile != newfile:
                if not os.path.exists(newfile):
                    shutil.move(oldfile, newfile)
                    print(f"移动文件: {filename} -> {folder_name}/")
                else:
                    print(f"文件已存在，跳过: {newfile}")
            break # 找到匹配分类后跳出循环

def classify_from_q(source_dir, q: Queue, type_to_classify):
    """
    消费者：从队列中取出目录和文件列表，进行分类并移动
    """
    while not q.empty():
        # 从队列里取出 (路径, 文件列表) 元组
        filepath, files = q.get()

        # 对每个文件进行处理
        for filename in files:
            move_to_newdir(source_dir, filename, filepath, type_to_classify)


# ==========================================
# 思考题解答：按照文件大小分类显示
# ==========================================
def classify_by_size(target_dir):
    """
    思考题：按照文件大小将文件分为“大于1GB”、“1GB到100MB”、“小于100MB”三类并显示
    """
    print("\n--- 思考题：按文件大小分类 ---")
    size_large = []   # > 1GB
    size_medium = []  # 100MB ~ 1GB
    size_small = []   # < 100MB
    
    gb_in_bytes = 1024 * 1024 * 1024
    mb_in_bytes = 100 * 1024 * 1024
    
    for root, dirs, files in os.walk(target_dir):
        for file in files:
            filepath = os.path.join(root, file)
            try:
                size = os.path.getsize(filepath)
                if size > gb_in_bytes:
                    size_large.append((file, size))
                elif size >= mb_in_bytes:
                    size_medium.append((file, size))
                else:
                    size_small.append((file, size))
            except OSError:
                pass # 忽略无法获取大小的文件（如权限问题）
                
    print(f"大于 1GB 的文件 ({len(size_large)} 个):")
    for f, s in size_large:
        print(f"  - {f} ({s / gb_in_bytes:.2f} GB)")
        
    print(f"\n100MB 到 1GB 的文件 ({len(size_medium)} 个):")
    for f, s in size_medium:
        print(f"  - {f} ({s / (1024*1024):.2f} MB)")
        
    print(f"\n小于 100MB 的文件 ({len(size_small)} 个):")
    for f, s in size_small[:10]: # 只显示前10个避免刷屏
        print(f"  - {f} ({s / 1024:.2f} KB)")
    if len(size_small) > 10:
        print(f"  ... (省略显示剩余 {len(size_small) - 10} 个文件)")


if __name__ == "__main__":
    # ================= 配置区域 =================
    # 定义要对哪个目录进行文件扩展名分类 (请修改为您实际的测试目录)
    SOURCE_DIR = "/Users/edz/Desktop/files"
    
    # 定义文件类型和它的扩展名
    FILE_TYPE_RULES = {
        "music": ("mp3", "wav"),
        "movie": ("mp4", "rmvb", "rm", "avi"),
        "execute": ("exe", "bat")
    }
    # ============================================

    if os.path.exists(SOURCE_DIR):
        print(f"开始对目录 {SOURCE_DIR} 进行分类...")

        # 1. 建立新的文件夹
        make_new_dir(SOURCE_DIR, FILE_TYPE_RULES)

        # 2. 定义一个用于记录扩展名放在指定目录的队列
        filename_q = Queue()

        # 3. 遍历目录并存入队列 (生产者)
        write_to_q(SOURCE_DIR, filename_q)

        # 4. 将队列的文件名分类并写入新的文件夹 (消费者)
        classify_from_q(SOURCE_DIR, filename_q, FILE_TYPE_RULES)
        
        print("文件分类完成！")
        
        # 5. 执行思考题逻辑
        classify_by_size(SOURCE_DIR)
    else:
        print(f"指定的目录不存在: {SOURCE_DIR}，请修改 SOURCE_DIR 后重试。")
