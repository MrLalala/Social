# coding: utf-8
from django.contrib.contenttypes.models import ContentType
from .models import Action
from django.utils import timezone
import datetime


def create_action(user, verb, target=None):
    # 获取当前时区时间
    now = timezone.now()
    # 获取当前时间往前推60的时间
    last_minute = now - datetime.timedelta(seconds=60)
    # 从Action中过滤在一分钟内相同id，描述的动作。
    similar_actions = Action.objects.filter(user_id=user.id, verb=verb,
                                            created__gte=last_minute)

    if target:
        target_ct = ContentType.objects.get_for_model(target)
        similar_actions = similar_actions.filter(target_ct=target_ct,
                                                 target_id=target.id)
    if not similar_actions:
        action = Action(user=user, verb=verb, target=target)
        action.save()
        return True
    return False
