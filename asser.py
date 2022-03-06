from telethon import events
from .. import loader, utils
import asyncio, re
chat = 707693258


@loader.tds
class AsserMod(loader.Module):
    """easy as lists and as in PM."""
    strings={"name": "as"}

    async def ascmd(self, message):
        """use: .ас to fast add in as list."""

        reply = await message.get_reply_message()
        send_mes = True
        sms = ""
        check_work = "⏳processing..."
        ids = []
        txt = reply.raw_text
        args = utils.get_args_raw(message)
        await utils.answer(message, check_work)
        while send_mes:
            send_mes = re.search(r"(?P<link>@[0-9a-z_]+|(?:https?://)?t\.me/[0-9a-z_]+|tg://openmessage\?user_id=(?P<id>[0-9]+))", txt, flags=re.I)
            if send_mes:
                txt = txt[send_mes.end():]
                send_mes = send_mes.groupdict()
                send_mes['link'], send_mes['id'] = '@'+send_mes['id'] if send_mes['id'] else send_mes['link'], ''
                mes = ''.join(send_mes.values())
                ids.append(mes)

        async with message.client.conversation(chat) as conv:
            for i in ids:
                response = conv.wait_event(events.NewMessage(incoming=True, from_users=chat, chats=chat))
                await message.client.send_message(chat, 'баны ' + i)
                response = await response
                if response.raw_text.lower().find('он в списке «ирис-антиспам»') != -1:
                    sms += '\n❌ ' + f"<code>{i}</code>"
                    await response.forward_to(message.to_id)
                else:
                    await asyncio.sleep(4)
                    await message.client.send_message(chat, f"+ас {i}\n{args}")
                    sms += '\n✅ ' + f"<code>{i}</code>"
                await utils.answer(message, check_work + sms)
                await asyncio.sleep(4)
            check_work = "checked!⌛️"
            await utils.answer(message, check_work+sms)
