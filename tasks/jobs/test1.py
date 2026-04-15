import os
import shutil
from datetime import datetime

from celery.utils.log import get_task_logger

from tasks import app
from tasks import config as cfg

logger = get_task_logger(__name__)


@app.task
def run1():
    """
    定时备份 data 目录（对应课程：每周六 22:01 备份 c:\\data）。
    将源目录打成 zip，写入 BACKUP_OUTPUT；源目录不存在时记录日志并跳过。
    """
    src = cfg.BACKUP_DIR_1
    out_dir = cfg.BACKUP_OUTPUT
    os.makedirs(out_dir, exist_ok=True)

    if not os.path.isdir(src):
        msg = f"源目录不存在，跳过备份: {src}"
        logger.warning(msg)
        return msg

    stamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    archive_base = os.path.join(out_dir, f"data_backup_{stamp}")
    shutil.make_archive(archive_base, "zip", root_dir=src)
    zip_path = archive_base + ".zip"
    msg = f"备份完成: {zip_path}"
    logger.info(msg)
    return msg
