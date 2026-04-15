import os
import argparse

def rename(file_path, old_ext):
    """批量改名函数"""
    if not os.path.exists(file_path):
        print(f"指定的目录不存在: {file_path}")
        return

    # 取得指定文件夹下的文件列表
    old_names = os.listdir(file_path)
    # 新文件名称从1开始
    new_name = 1

    # 取得所有的文件名
    for old_name in old_names:
        # 根据扩展名，判断文件是否需要改名
        if old_name.endswith(old_ext):
            # 完整的文件路径
            old_path = os.path.join(file_path, old_name)
            # 新的文件名
            new_path = os.path.join(file_path, str(new_name) + old_ext)
            
            # 避免覆盖已存在的文件
            while os.path.exists(new_path) and old_path != new_path:
                new_name += 1
                new_path = os.path.join(file_path, str(new_name) + old_ext)
                
            # 重命名
            if old_path != new_path:
                os.rename(old_path, new_path)
                print(f"重命名: {old_name} -> {str(new_name) + old_ext}")
            
            # 文件名数字加1
            new_name += 1

def args_opt():
    """获取命令行参数函数"""
    # 定义参数对象
    parser = argparse.ArgumentParser(description="批量重命名指定扩展名的文件")
    
    # 增加参数选项、是否必须、帮助信息
    parser.add_argument("-p", "--path", required=True, help="path to rename (要重命名的目录路径)")
    parser.add_argument("-e", "--ext", required=True, help="files name extension, eg: jpg (文件扩展名，如 jpg)")
    
    # 返回取得的所有参数
    return parser.parse_args()

if __name__ == "__main__":
    # args 对象包含所有参数，属性是命令行参数的完整名称
    args = args_opt()
    
    # 确保扩展名前面有 "."
    ext = args.ext if args.ext.startswith(".") else "." + args.ext
    
    # 调用重命名函数，将命令行参数作为重命名函数的参数
    rename(args.path, ext)
    
    # 输出改名之后的结果
    if os.path.exists(args.path):
        print("\n改名之后的结果:")
        print(os.listdir(args.path))
