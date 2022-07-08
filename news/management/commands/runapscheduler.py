# news/management/commands/runapscheduler.py

# ===============================================
# планировщик заданий
# ===============================================

from django.conf import settings
from loguru import logger
from apscheduler.schedulers.blocking import BlockingScheduler
from apscheduler.triggers.cron import CronTrigger
from django.core.management.base import BaseCommand
from django_apscheduler.jobstores import DjangoJobStore
from django_apscheduler.models import DjangoJobExecution
from ...utils import mailing_week_report


# ===============================================
# функция, которая будет удалять неактуальные задачи
# ===============================================
def delete_old_job_executions(max_age=604_800):

    # удаляет все выполненные задачи из базы старше max_age
    DjangoJobExecution.objects.delete_old_job_executions(max_age)


# ===============================================
# тестовая задача для контроля работы планировщика
# ===============================================
def test_job():
    print('Hello, World!')


# ===============================================
# коммандер планировщика
# ===============================================
class Command(BaseCommand):
    help = "Runs apscheduler."

    def handle(self, *args, **options):

        scheduler = BlockingScheduler(timezone=settings.TIME_ZONE)
        scheduler.add_jobstore(DjangoJobStore(), "default")

        # добавляем работу
        scheduler.add_job(

            # тестовая работа
            test_job,

            # каждые 10 секунд
            trigger=CronTrigger(second="*/10"),

            id="test_job",
            max_instances=1,
            replace_existing=True,
        )
        logger.info("Added job 'test_job'.")

        # добавляем работу
        scheduler.add_job(

            # еженедельная рассылка отчетов
            mailing_week_report,

            # по воскресеньям
            trigger=CronTrigger(day_of_week="sun", hour="00", minute="00"),

            id="mailing_week_report",
            max_instances=1,
            replace_existing=True,
        )
        logger.info("Added weekly job 'mailing_week_report'")

        # добавляем работу
        scheduler.add_job(

            # будут удаляться старые задачи,
            # которые либо не удалось выполнить, либо уже выполнять не надо.
            delete_old_job_executions,

            # По понедельникам
            trigger=CronTrigger(day_of_week="mon", hour="00", minute="00"),

            id="delete_old_job_executions",
            max_instances=1,
            replace_existing=True,
        )
        logger.info("Added weekly job: 'delete_old_job_executions'.")

        # старт планировщика
        try:
            logger.info("Starting scheduler...")
            scheduler.start()

        # остановка по команде клавиатуры
        except KeyboardInterrupt:
            logger.info("Stopping scheduler...")
            scheduler.shutdown()
            logger.info("Scheduler shut down successfully!")
