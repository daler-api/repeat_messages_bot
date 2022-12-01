import datetime
import re
import time

import zulip
from dateutil.relativedelta import relativedelta
from django.core.exceptions import ValidationError

from repeat_messages_bot.settings import BASE_DIR


def get_valid_names(url):
    "https://chat.zulip.org/#narrow/stream/9-issues/topic/LDAP.20Sync"
    core_url = url.replace("https://chat.zulip.org/#narrow/stream/", '')[1:]
    core_url = core_url[1:].split('/')
    stream_name = core_url[0]
    topic_name = core_url[2].replace('.20', " ").replace("2E", '')
    return stream_name, topic_name


def parse_info(stream, topic, days_ago, load_stream_name, load_topic_name):
    file = BASE_DIR / 'core/key/zulip'
    client = zulip.Client(config_file=file)
    result = client.add_subscriptions(
        streams=[
            {
                "name": stream
            },
        ],
    )
    if result['result'] == 'success':
        request = {
            "anchor": "newest",
            "num_before": 5000,
            "num_after": 0,
            "narrow": [
                {"operator": "stream", "operand": stream},
                {"operator": "topic", "operand": topic}
            ],
        }
        result = client.get_messages(request)
        now = datetime.datetime.now().strftime('%Y-%m-%d').split('-')
        now = [int(x) for x in now]
        now = datetime.date(year=now[0], month=now[1], day=now[2])
        print("Сегодня", now)
        period = now - relativedelta(days=days_ago)
        print("6 месяцев назад", period)
        for message in result['messages']:

            date = datetime.datetime.fromtimestamp(message['timestamp']).strftime('%Y-%m-%d').split('-')
            date = [int(x) for x in date]
            date = datetime.date(year=date[0], month=date[1], day=date[2])
            print(date)
            if date == period:
                text = re.sub(r'\<[^>]*\>', '', message['content'])
                request = {
                    "type": "stream",
                    "to": load_stream_name,
                    "topic": load_topic_name,
                    "content": text,
                }
                result = client.send_message(request)
                print(result)
    else:
        raise ValidationError('Что то пошло не так пожалуйста попробуйте еще раз')
