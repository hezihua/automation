import os
import datetime
from zipfile import ZipFile

# 遍历目录，得到该目录下所有的子目录和文件
def getAllFiles(dir_path):
    for root, dirs, files in os.walk(dir_path):
        for file in files:
            # 使用 yield 构造生成器，避免一次性加载大量文件路径导致内存占用过高
            yield os.path.join(root, file)

# 以年月日作为zip文件名
def genZipfilename():
    today = datetime.date.today()
    basename = today.strftime('%Y%m%d')
    extname = "zip"
    return f"{basename}.{extname}"

# 无密码生成压缩文件
def zipWithoutPassword(files, backupFilename):
    print(f"正在使用 zipfile 创建无密码压缩包: {backupFilename}")
    with ZipFile(backupFilename, 'w') as zf:
        for f in files:
            # 写入文件，这里可以根据需要调整 arcname 参数以改变压缩包内的目录结构
            zf.write(f)
    print("无密码压缩完成！")

# 使用 7z 命令实现有密码压缩文件
# 注意：运行此函数需要系统中已安装 7-Zip，并且 7z.exe 已加入到系统环境变量 Path 中。
def zipWithPassword(dir_path, backupFilename, password=None):
    print(f"正在使用 7z 创建加密压缩包: {backupFilename}")
    # 构造 7z 压缩命令
    # a: 添加到压缩包
    # -tzip: 指定压缩格式为 zip
    # -p: 指定密码
    cmd = f'7z.exe a -tzip "{backupFilename}" -p"{password}" "{dir_path}"'
    
    # 使用 os.popen 执行命令并获取执行状态/输出
    with os.popen(cmd) as status:
        output = status.read()
        print(output)
    print("加密压缩完成！")

if __name__ == '__main__':
    # ================= 配置区域 =================
    # 要备份的目录 (请修改为实际存在的目录路径)
    backupDir = r"C:\data"
    
    # 压缩包密码
    zipPassword = "password123"
    # ============================================

    # 确保备份目录存在，否则直接退出
    if not os.path.exists(backupDir):
        print(f"指定的备份目录不存在: {backupDir}")
    else:
        # zip文件的名字“年月日.zip”
        zipFilename = genZipfilename()
        
        # ---------------------------------------------------------
        # 方式一：无密码压缩 (使用 Python 内置 zipfile 库)
        # ---------------------------------------------------------
        # 获取要备份的文件生成器
        backupFiles = getAllFiles(backupDir)
        # 为了区分两种方式生成的文件，给无密码的压缩包加个后缀
        unencrypted_zip = f"unencrypted_{zipFilename}"
        zipWithoutPassword(backupFiles, unencrypted_zip)
        
        # ---------------------------------------------------------
        # 方式二：有密码压缩 (调用外部 7z.exe 命令)
        # ---------------------------------------------------------
        # 为了区分两种方式生成的文件，给有密码的压缩包加个后缀
        encrypted_zip = f"encrypted_{zipFilename}"
        zipWithPassword(backupDir, encrypted_zip, zipPassword)
        
        # ---------------------------------------------------------
        # 思考题解答：如果需要备份多个目录，可以怎么改造？
        # ---------------------------------------------------------
        # 思路：可以将 backupDir 改为一个列表，然后遍历这个列表。
        # 对于 zipfile：
        # dirs_to_backup = [r"C:\data1", r"C:\data2"]
        # with ZipFile(zipFilename, 'w') as zf:
        #     for d in dirs_to_backup:
        #         for f in getAllFiles(d):
        #             zf.write(f)
        # 
        # 对于 7z 命令：
        # dirs_str = " ".join([f'"{d}"' for d in dirs_to_backup])
        # cmd = f'7z.exe a -tzip "{backupFilename}" -p"{password}" {dirs_str}'
