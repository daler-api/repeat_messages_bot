import datetime
import re
import time

from django.core.management.base import BaseCommand
import zulip
from dateutil.relativedelta import relativedelta
from repeat_messages_bot.settings import BASE_DIR


class Command(BaseCommand):
    help = 'Closes the specified poll for voting'

    def handle(self, *args, **options):
        file = BASE_DIR / 'core/key/zulip'
        client = zulip.Client(config_file=file)
        result = client.add_subscriptions(
            streams=[
                {
                    "name": "general"
                },
            ],
        )
        print(result)
        request = {
            "anchor": "newest",
            "num_before": 5000,
            "num_after": 0,
            "narrow": [
                {"operator": "stream", "operand": "general"},
                {"operator": "topic", "operand": "sales"}
            ],
        }
        result = client.get_messages(request)
        now = datetime.datetime.now().strftime('%Y-%m-%d').split('-')
        now = [int(x) for x in now]
        now = datetime.date(year=now[0], month=now[1], day=now[2])
        print("Сегодня", now)
        period = now - relativedelta(days=7)
        print("6 месяцев назад", period)
        for message in result['messages']:
            date = datetime.datetime.fromtimestamp(message['timestamp']).strftime('%Y-%m-%d').split('-')
            date = [int(x) for x in date]
            date = datetime.date(year=date[0], month=date[1], day=date[2])
            if date == period:
                text = re.sub(r'\<[^>]*\>', '', message['content'])
                request = {
                    "type": "stream",
                    "to": "general",
                    "topic": "reply sales",
                    "content": text,
                }
                result = client.send_message(request)
                print(result)
        time.sleep(2)

