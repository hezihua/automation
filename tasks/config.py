import os

from celery.schedules import crontab

# 项目根目录（automation/）
PROJECT_ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

# Redis 作为 Broker；可用环境变量覆盖
broker_url = os.environ.get("CELERY_BROKER_URL", "redis://127.0.0.1:6379/1")

# 时区（与课程一致）
timezone = "Asia/Shanghai"

# 需要加载的任务模块（对应课程中的 imports）
imports = [
    "tasks.jobs.test1",
    "tasks.jobs.test2",
]

# 待备份的源目录（默认在项目下 data / data2，可通过环境变量覆盖）
BACKUP_DIR_1 = os.environ.get(
    "CELERY_BACKUP_SOURCE_1", os.path.join(PROJECT_ROOT, "data")
)
BACKUP_DIR_2 = os.environ.get(
    "CELERY_BACKUP_SOURCE_2", os.path.join(PROJECT_ROOT, "data2")
)
# 备份 zip 输出目录
BACKUP_OUTPUT = os.environ.get(
    "CELERY_BACKUP_OUTPUT", os.path.join(PROJECT_ROOT, "backups")
)

# 定时任务：test1 每周六 22:01；test2 每分钟（便于快速观察 Worker 输出）
# 思考题参考：每周一、三、五 18:00 提交报告可用：
#   crontab(minute=0, hour=18, day_of_week="mon,wed,fri")
beat_schedule = {
    "test1": {
        "task": "tasks.jobs.test1.run1",
        "schedule": crontab(minute=1, hour=22, day_of_week=6),
        "args": (),
    },
    "test2": {
        "task": "tasks.jobs.test2.run1",
        "schedule": crontab(minute="*"),
        "args": (),
    },
}
