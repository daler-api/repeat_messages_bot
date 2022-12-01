import os

from apscheduler.triggers.cron import CronTrigger
from django.contrib import admin
from core.helpers import get_valid_names, parse_info
from core.models import Newsletter
from core.scheduler.start import scheduler


@admin.register(Newsletter)
class NewsletterAdmin(admin.ModelAdmin):
    list_display = ['topic_parser', 'topic_donor', 'post_datetime']

    def save_model(self, request, obj, form, change):
        super(NewsletterAdmin, self).save_model(request, obj, form, change)

        post_time = obj.post_datetime.strftime("%H-%M-%S").split('-')
        stream_name, topic_name = get_valid_names(obj.topic_parser)
        load_stream_name, load_topic_name = get_valid_names(obj.topic_donor)

        scheduler.add_job(
            parse_info,
            trigger=CronTrigger(
                hour=post_time[0],
                minute=post_time[1],
                second=post_time[2]
            ),
            args=[stream_name, topic_name, obj.days_ago, load_stream_name, load_topic_name]
        )
        os.system('systemctl restart repeat_bot')
