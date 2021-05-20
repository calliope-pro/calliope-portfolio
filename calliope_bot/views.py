import os
import re

from django.contrib.auth import get_user_model
from django.core.exceptions import ObjectDoesNotExist
from django.http import HttpResponse, HttpResponseForbidden
from django.shortcuts import render
from django.utils import timezone
from django.views.decorators.csrf import csrf_exempt
from linebot import LineBotApi, WebhookHandler
from linebot.exceptions import InvalidSignatureError, LineBotApiError
from linebot.models import (FollowEvent, ImageMessage, ImageSendMessage,
                            MessageEvent, SendMessage, TextMessage,
                            TextSendMessage, UnfollowEvent)

from .models import LineProfile

line_bot_api = LineBotApi(os.environ['LINE_CHANNEL_ACCESS_TOKEN'])
handler = WebhookHandler(os.environ['LINE_CHANNEL_SECRET'])

@csrf_exempt
def callback(request):
    signature = request.META['HTTP_X_LINE_SIGNATURE']

    body = request.body.decode('utf-8')

    # handle webhook body
    try:
        handler.handle(body, signature)
    except InvalidSignatureError:
        HttpResponseForbidden()
        
    return HttpResponse('OK', status=200)


@handler.add(FollowEvent)
def handle_follow(event):
    line_user_id = event.source.user_id
    line_user, new_created = LineProfile.objects.get_create(line_id=line_user_id)
    line_profile = line_bot_api.get_profile(line_user_id)
    line_user.line_icon_url = line_profile.picture_url
    line_user.line_name = line_profile.display_name
    line_user.save()

@handler.add(MessageEvent, message=TextMessage)
def handle_message(event):
    REPLY_TOKEN = event.reply_token
    USER_ID = PUSH_REPLY_ID = event.source.user_id
    if event.source.type == 'room':
        PUSH_REPLY_ID = event.source.room_id
    elif event.source.type == 'group':
        PUSH_REPLY_ID = event.source.group_id

    txt = event.message.text.strip()
    res_txt = txt*2
    reply = [TextSendMessage(text=res_txt)]
        
    line_bot_api.reply_message(
        REPLY_TOKEN,
        reply
    )

