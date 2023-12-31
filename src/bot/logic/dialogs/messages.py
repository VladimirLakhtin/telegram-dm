"""Messages dialog file"""
from aiogram.enums import ContentType
from aiogram_dialog import Window, Dialog
from aiogram_dialog.widgets.input import MessageInput
from aiogram_dialog.widgets.kbd import Cancel, SwitchTo, Back, Row, Button, Select, Column, Next
from aiogram_dialog.widgets.text import Const, Format
from aiogram_dialog.widgets.media import DynamicMedia
from magic_filter import F

from src.bot.logic.handlers.messages import (
    input_message_text, confirm_create_message,
    input_message_title, message_details,
    delete_message, input_message_media, back_from_media_input,
)
from src.bot.structures.getters import get_message_data, get_messages_data, get_message_data_by_id
from src.bot.structures.states import MessagesStatesGroup
from src.bot.structures.text import ButtonText as btn_txt
from src.bot.structures.text import CaptureText as cpt_txt


lst_win = Window(
    Const(cpt_txt.MESSAGES_LIST),
    Column(
        Select(
            Format('{item.title}'),
            id='title',
            item_id_getter=lambda m: m.id,
            items=F['messages'],
            on_click=message_details,
        ),
    ),
    Row(
        SwitchTo(
            Const(btn_txt.MESSAGE_NEW),
            id='add',
            state=MessagesStatesGroup.input_title,
        ),
        Cancel(Const(btn_txt.BACK)),
    ),
    getter=get_messages_data,
    state=MessagesStatesGroup.lst,
)

details_win = Window(
    DynamicMedia(selector='media'),
    Format('<b>{message.title}</b>\n\n{message.text}'),
    Row(
        SwitchTo(
            Const(btn_txt.DELETE),
            state=MessagesStatesGroup.delete,
            id='delete',
        ),
        Back(Const(btn_txt.BACK)),
    ),
    getter=get_message_data_by_id,
    state=MessagesStatesGroup.details
)

input_title_win = Window(
    Const(cpt_txt.MESSAGE_TITLE_INPUT),
    Cancel(Const(btn_txt.BACK)),
    MessageInput(
        content_types=[ContentType.TEXT],
        func=input_message_title,
    ),
    state=MessagesStatesGroup.input_title,
)

input_text_win = Window(
    Const(cpt_txt.MESSAGE_TEXT_INPUT),
    Back(Const(btn_txt.BACK)),
    MessageInput(
        content_types=[ContentType.TEXT],
        func=input_message_text,
    ),
    state=MessagesStatesGroup.input_text,
)

input_media_win = Window(
    Const(cpt_txt.MESSAGE_MEDIA_INPUT),
    Row(
        Next(Const(btn_txt.SKIP)),
        Back(Const(btn_txt.BACK)),
    ),
    MessageInput(
        content_types=[ContentType.PHOTO, ContentType.VIDEO],
        func=input_message_media,
    ),
    state=MessagesStatesGroup.input_media,
)

confirm_add_win = Window(
    DynamicMedia(selector='media'),
    Format(cpt_txt.MESSAGE_ADD_CONFIRM),
    Row(
        Button(
            Const(btn_txt.CONFIRM),
            id="yes",
            on_click=confirm_create_message,
        ),
        SwitchTo(
            Const(btn_txt.REJECT),
            id='no',
            state=MessagesStatesGroup.lst,
            on_click=back_from_media_input,
        ),
    ),
    state=MessagesStatesGroup.add,
    getter=get_message_data,
)

confirm_delete_win = Window(
    Format(cpt_txt.MESSAGE_DELETE_CONFIRM),
    Row(
        Button(
            Const(btn_txt.CONFIRM),
            id="yes",
            on_click=delete_message,
        ),
        SwitchTo(
            Const(btn_txt.REJECT),
            id='no',
            state=MessagesStatesGroup.lst,
        ),
    ),
    state=MessagesStatesGroup.delete,
    getter=get_message_data_by_id,
)

dialog = Dialog(
    lst_win,
    details_win,
    input_title_win,
    input_text_win,
    input_media_win,
    confirm_add_win,
    confirm_delete_win,
)
