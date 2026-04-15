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
    每分钟执行一次（课程示例 test2），备份 data2 目录。
    """
    src = cfg.BACKUP_DIR_2
    out_dir = cfg.BACKUP_OUTPUT
    os.makedirs(out_dir, exist_ok=True)

    if not os.path.isdir(src):
        msg = f"源目录不存在，跳过备份: {src}"
        logger.warning(msg)
        return msg

    stamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    archive_base = os.path.join(out_dir, f"data2_backup_{stamp}")
    shutil.make_archive(archive_base, "zip", root_dir=src)
    zip_path = archive_base + ".zip"
    msg = f"备份完成: {zip_path}"
    logger.info(msg)
    return msg
