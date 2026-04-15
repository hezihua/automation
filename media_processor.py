import os
from pathlib import Path, PurePath
from subprocess import run

# ==============================================================================
# 注意：本脚本基于 Python 内置的 subprocess 模块调用外部命令行工具。
# 运行本脚本前，请确保您的系统中已安装以下外部软件，并已将其添加到环境变量 Path 中：
# 1. ImageMagick (用于图片拼接，提供 composite/convert 命令)
# 2. FFmpeg (用于视频拆分与合并，提供 ffmpeg 命令)
# ==============================================================================

def stitch_images(input_dir, result_path):
    """
    长图拼接：使用 ImageMagick 将目录下的多张 jpg 图片拼接成一张长图。
    注意：原教程中演示使用的是 `composite` 命令，但实际 ImageMagick 中
    垂直拼接通常使用 `convert -append` 或 `magick -append`。
    这里为了遵循教程的思路，展示如何用 subprocess 动态拼接不定数量的参数。
    """
    print(f"\n--- 开始图片拼接 ---")
    p = Path(input_dir)
    
    if not p.exists():
        print(f"图片目录不存在: {input_dir}")
        return

    # 基础命令 (这里使用 convert -append 演示更通用的垂直长图拼接)
    # 如果您的 ImageMagick 版本较新(v7+)，建议将 "convert" 替换为 "magick"
    cmd = ["convert", "-append"]

    # 动态增加参数：遍历目录下所有的 .jpg 文件
    # 修复了原教程中 for 循环和 if 连写的语法错误
    image_files = []
    for x in p.iterdir():
        if PurePath(x).match('*.jpg') or PurePath(x).match('*.png'):
            image_files.append(str(x))
            
    # 为了保证拼接顺序，可以对文件名进行排序
    image_files.sort()
    cmd.extend(image_files)

    # 增加输出结果路径
    cmd.append(result_path)

    print(f"执行命令: {' '.join(cmd)}")
    try:
        # 执行外部命令
        run(cmd, check=True)
        print(f"图片拼接成功，结果保存至: {result_path}")
    except Exception as e:
        print(f"图片拼接失败 (请确认已安装 ImageMagick): {e}")


def split_video(input_video, m3u8_list, output_video_pattern, segment_time=10):
    """
    视频拆分：使用 FFmpeg 将 MP4 视频切分为多个 TS 文件，并生成 m3u8 索引。
    """
    print(f"\n--- 开始视频拆分 ---")
    if not os.path.exists(input_video):
        print(f"输入视频不存在: {input_video}")
        return

    cmd = [
        "ffmpeg", 
        "-i", input_video, 
        "-f", "segment", 
        "-segment_time", str(segment_time), 
        "-segment_format", "mpegts", 
        "-segment_list", m3u8_list, 
        "-c", "copy", 
        "-bsf:v", "h264_mp4toannexb", 
        "-map", "0", 
        output_video_pattern
    ]

    print(f"执行命令: {' '.join(cmd)}")
    try:
        run(cmd, check=True)
        print(f"视频拆分成功，索引文件保存至: {m3u8_list}")
    except Exception as e:
        print(f"视频拆分失败 (请确认已安装 FFmpeg): {e}")


def merge_video(input_m3u8, output_mp4):
    """
    视频合并：使用 FFmpeg 将 m3u8 索引及对应的 TS 分段文件合并为一个 MP4 视频。
    """
    print(f"\n--- 开始视频合并 ---")
    if not os.path.exists(input_m3u8):
        print(f"索引文件不存在: {input_m3u8}")
        return

    cmd = [
        "ffmpeg", 
        "-allowed_extensions", "ALL", 
        "-protocol_whitelist", "file,http,crypto,tcp,https", 
        "-i", input_m3u8, 
        "-c", "copy", 
        output_mp4
    ]

    print(f"执行命令: {' '.join(cmd)}")
    try:
        run(cmd, check=True)
        print(f"视频合并成功，结果保存至: {output_mp4}")
    except Exception as e:
        print(f"视频合并失败 (请确认已安装 FFmpeg): {e}")


if __name__ == "__main__":
    # ================= 配置区域 =================
    # 1. 长图拼接配置
    IMAGE_INPUT_DIR = "./images_to_stitch"
    IMAGE_OUTPUT = "./stitched_result.jpg"
    
    # 2. 视频拆分配置
    VIDEO_TO_SPLIT = "./sample_video.mp4"
    M3U8_OUTPUT = "./playlist.m3u8"
    TS_OUTPUT_PATTERN = "./video-%04d.ts" # %04d 会自动替换为 0000, 0001 等序号
    
    # 3. 视频合并配置 (将上面拆分出的 m3u8 重新合并)
    MERGED_VIDEO_OUTPUT = "./merged_video.mp4"
    # ============================================

    print("=== 多媒体处理自动化脚本 (基于 subprocess) ===")
    
    # 提示：由于没有实际的测试文件和外部软件环境，这里仅展示函数调用逻辑。
    # 在实际使用时，请确保配置的路径下有对应的文件。
    
    # 1. 测试长图拼接
    # stitch_images(IMAGE_INPUT_DIR, IMAGE_OUTPUT)
    
    # 2. 测试视频拆分
    # split_video(VIDEO_TO_SPLIT, M3U8_OUTPUT, TS_OUTPUT_PATTERN, segment_time=10)
    
    # 3. 测试视频合并
    # merge_video(M3U8_OUTPUT, MERGED_VIDEO_OUTPUT)
    
    print("\n脚本执行完毕。请取消注释相应的函数调用，并准备好测试文件后运行。")
