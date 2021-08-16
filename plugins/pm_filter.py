#Kanged From @TroJanZheX
from info import AUTH_CHANNEL, AUTH_USERS, CUSTOM_FILE_CAPTION, API_KEY, AUTH_GROUPS, FILTER_PIC, MAIN_LINK
from pyrogram.types import InlineKeyboardMarkup, InlineKeyboardButton, CallbackQuery
from pyrogram import Client, filters
import re
from pyrogram.errors import UserNotParticipant
from utils import get_filter_results, get_file_details, is_subscribed, get_poster
from db.users import present_in_userbase, add_to_userbase
BUTTONS = {}
BOT = {}
@Client.on_message(filters.text & filters.private & filters.incoming & filters.user(AUTH_USERS) if AUTH_USERS else filters.text & filters.private & filters.incoming)
async def filter(client, message):
    if not await present_in_userbase(message.from_user.id):
        await add_to_userbase(message.from_user.id)
    if message.text.startswith("/"):
        return
    if AUTH_CHANNEL:
        invite_link = await client.create_chat_invite_link(int(AUTH_CHANNEL))
        try:
            user = await client.get_chat_member(int(AUTH_CHANNEL), message.from_user.id)
            if user.status == "kicked":
                await client.send_message(
                    chat_id=message.from_user.id,
                    text="Sorry Sir, You are Banned to use me.",
                    parse_mode="markdown",
                    disable_web_page_preview=True
                )
                return
        except UserNotParticipant:
            await client.send_message(
                chat_id=message.from_user.id,
                text=f"**♦️ READ THIS INSTRUCTION ♦️**\n\n__🗣 നിങ്ങൾ ചോദിക്കുന്ന സിനിമകൾ നിങ്ങൾക്ക് ലഭിക്കണം എന്നുണ്ടെങ്കിൽ നിങ്ങൾ താഴെ കൊടുത്തിട്ടുള്ള ചാനലിൽ ജോയിൻ ചെയ്യണം. ജോയിൻ ചെയ്ത ശേഷം വീണ്ടും ഗ്രൂപ്പിൽ പോയി ആ ബട്ടനിൽ അമർത്തിയാൽ നിങ്ങൾക്ക് ഞാൻ ആ സിനിമ പ്രൈവറ്റ് ആയി അയച്ചു തരുന്നതാണ്..😍\n\n🗣 In Order To Get The Movie Requested By You in Our Groups, You Will Have To Join Our Official Channel First. After That, Try Accessing That Movie Again From Our Group. I'll Send You That Movie Privately 🙈__\n\n**👇 JOIN THIS CHANNEL & TRY 👇\n\n[{MAIN_LINK}]**",
                reply_markup=InlineKeyboardMarkup(
                    [
                        [
                            InlineKeyboardButton("💢𝙹𝚘𝚒𝚗 𝙼𝚢 𝙲𝚑𝚊𝚗𝚗𝚎𝚕💢", url=invite_link.invite_link)
                        ]
                    ]
                ),
                parse_mode="markdown",
                disable_web_page_preview=True
            )
            return
        except Exception:
            await client.send_message(
                chat_id=message.from_user.id,
                text="Something went Wrong.",
                parse_mode="markdown",
                disable_web_page_preview=True
            )
            return
    if re.findall("((^\/|^,|^!|^\.|^[\U0001F600-\U000E007F]).*)", message.text):
        return
    if 2 < len(message.text) < 100:    
        btn = []
        search = message.text
        files = await get_filter_results(query=search)
        btn.append(
            [InlineKeyboardButton("💢 𝗝𝗼𝗶𝗻 𝗢𝘂𝗿 𝗠𝗮𝗶𝗻 𝗰𝗵𝗮𝗻𝗻𝗲𝗹 💢", url=invite_link.invite_link)]
        )
        if files:
            for file in files:
                file_id = file.file_id
                filename = f"[{get_size(file.file_size)}] {file.file_name}"
                btn.append(
                    [InlineKeyboardButton(text=f"{filename}",callback_data=f"subinps#{file_id}")]
                    )
        else:
            await client.send_sticker(chat_id=message.from_user.id, sticker='CAADBQADMwIAAtbcmFelnLaGAZhgBwI')
            return

        if not btn:
            return

        if len(btn) > 10: 
            btns = list(split_list(btn, 10)) 
            keyword = f"{message.chat.id}-{message.message_id}"
            BUTTONS[keyword] = {
                "total" : len(btns),
                "buttons" : btns
            }
        else:
            buttons = btn
            buttons.append(
                [InlineKeyboardButton(text="📃 Pages 1/1",callback_data="pages")]
            )
         #   buttons.append(
               # [InlineKeyboardButton("✨️𝐒𝐞𝐫𝐢𝐞𝐬 𝐒𝐭𝐮𝐝𝐢𝐨✨️", url="https://t.me/Series_Studio")]
          #  )
            poster=None
            if API_KEY:
                poster=await get_poster(search)
            if poster:
                await message.reply_photo(photo=poster, caption=f"<b>Total Files:</b><code>{len(files)}</code>\n<b>Movie Name:</b> <code>{search}</code>\n\n<b>© 𝐐𝐮𝐚𝐥𝐢𝐭𝐲 𝐌𝐨𝐭𝐢𝐨𝐧 𝐏𝐢𝐜𝐭𝐮𝐫𝐞𝐬</b>", reply_markup=InlineKeyboardMarkup(buttons))
            else:
                await message.reply_photo(photo=FILTER_PIC, caption=f"<b>Total Files:</b><code>{len(files)}</code>\n<b>Movie Name:</b> <code>{search}</code>\n\n<b>© 𝐐𝐮𝐚𝐥𝐢𝐭𝐲 𝐌𝐨𝐭𝐢𝐨𝐧 𝐏𝐢𝐜𝐭𝐮𝐫𝐞𝐬</b>", reply_markup=InlineKeyboardMarkup(buttons))
            return

        data = BUTTONS[keyword]
        buttons = data['buttons'][0].copy()

        buttons.append(
            [InlineKeyboardButton(text="NEXT ⏩",callback_data=f"next_0_{keyword}")]
        )    
        buttons.append(
            [InlineKeyboardButton(text=f"📃 Pages 1/{data['total']}",callback_data="pages")]
        )
       # buttons.append(
            #[InlineKeyboardButton("✨️𝐒𝐞𝐫𝐢𝐞𝐬 𝐒𝐭𝐮𝐝𝐢𝐨✨️", url="https://t.me/Series_Studio")]
      #  )
        poster=None
        if API_KEY:
            poster=await get_poster(search)
        if poster:
            await message.reply_photo(photo=poster, caption=f"<b>Total Files:</b><code>{len(files)}</code>\n<b>Movie Name:</b> <code>{search}</code>\n\n<b© 𝐐𝐮𝐚𝐥𝐢𝐭𝐲 𝐌h𝐨𝐭𝐢𝐨𝐧 𝐏𝐢𝐜𝐭𝐮𝐫𝐞𝐬</b>", reply_markup=InlineKeyboardMarkup(buttons))
        else:
            await message.reply_photo(photo=FILTER_PIC, caption=f"<b>Total Files:</b><code>{len(files)}</code>\n<b>Movie Name:</b> <code>{search}</code>\n\n<b>© 𝐐𝐮𝐚𝐥𝐢𝐭𝐲 𝐌𝐨𝐭𝐢𝐨𝐧 𝐏𝐢𝐜𝐭𝐮𝐫𝐞𝐬</b>", reply_markup=InlineKeyboardMarkup(buttons))

    if not await present_in_userbase(message.from_user.id):
        await add_to_userbase(message.from_user.id)

@Client.on_message(filters.text & filters.group & filters.incoming & filters.chat(AUTH_GROUPS) if AUTH_GROUPS else filters.text & filters.group & filters.incoming)
async def group(client, message):
    if re.findall("((^\/|^,|^!|^\.|^[\U0001F600-\U000E007F]).*)", message.text):
        return
    if 2 < len(message.text) < 50:    
        btn = []
        search = message.text
        nyva=BOT.get("username")
        if not nyva:
            botusername=await client.get_me()
            nyva=botusername.username
            BOT["username"]=nyva
        files = await get_filter_results(query=search)
        btn.append(
               [InlineKeyboardButton("💢 𝗝𝗼𝗶𝗻 𝗢𝘂𝗿 𝗠𝗮𝗶𝗻 𝗰𝗵𝗮𝗻𝗻𝗲𝗹 💢", url=f"{MAIN_LINK}")]
           )
        if files:
            for file in files:
                file_id = file.file_id
                filename = f"[{get_size(file.file_size)}] {file.file_name}"
                btn.append(
                    [InlineKeyboardButton(text=f"{filename}", url=f"https://telegram.dog/{nyva}?start=qmp_cinemas_-_-_-_{file_id}")]
                )
        else:
            return
        if not btn:
            return

        if len(btn) > 10: 
            btns = list(split_list(btn, 10)) 
            keyword = f"{message.chat.id}-{message.message_id}"
            BUTTONS[keyword] = {
                "total" : len(btns),
                "buttons" : btns
            }
        else:
            buttons = btn
            buttons.append(
                [InlineKeyboardButton(text="📃 Pages 1/1",callback_data="pages")]
            )
         #   buttons.append(
               # [InlineKeyboardButton("✨️𝐒𝐞𝐫𝐢𝐞𝐬 𝐒𝐭𝐮𝐝𝐢𝐨✨️", url="https://t.me/Series_Studio")]
        #    )
            poster=None
            if API_KEY:
                poster=await get_poster(search)
            if poster:
                await message.reply_photo(photo=poster, caption=f"<b>Total Files:</b><code>{len(files)}</code>\n<b>Movie Name:</b> <code>{search}</code>\n\n<b© 𝐐𝐮𝐚𝐥𝐢𝐭𝐲 𝐌𝐨𝐭𝐢𝐨𝐧 𝐏𝐢𝐜𝐭𝐮𝐫𝐞𝐬</b>", reply_markup=InlineKeyboardMarkup(buttons))
            else:
                await message.reply_photo(photo=FILTER_PIC, caption=f"<b>Total Files:</b><code>{len(files)}</code>\n<b>Movie Name:</b> <code>{search}</code>\n\n<b>© 𝐐𝐮𝐚𝐥𝐢𝐭𝐲 𝐌𝐨𝐭𝐢𝐨𝐧 𝐏𝐢𝐜𝐭𝐮𝐫𝐞𝐬</b>", reply_markup=InlineKeyboardMarkup(buttons))
            return

        data = BUTTONS[keyword]
        buttons = data['buttons'][0].copy()

        buttons.append(
            [InlineKeyboardButton(text="NEXT ⏩",callback_data=f"next_0_{keyword}")]
        )    
        buttons.append(
            [InlineKeyboardButton(text=f"📃 Pages 1/{data['total']}",callback_data="pages")]
        )
     #   buttons.append(
          #  [InlineKeyboardButton("✨️𝐒𝐞𝐫𝐢𝐞𝐬 𝐒𝐭𝐮𝐝𝐢𝐨✨️", url="https://t.me/Series_Studio")]
        #    )
        poster=None
        if API_KEY:
            poster=await get_poster(search)
        if poster:
            await message.reply_photo(photo=poster, caption=f"<b>Total Files:</b><code>{len(files)}</code>\n<b>Movie Name:</b> <code>{search}</code>\n\n<b>© 𝐐𝐮𝐚𝐥𝐢𝐭𝐲 𝐌𝐨𝐭𝐢𝐨𝐧 𝐏𝐢𝐜𝐭𝐮𝐫𝐞𝐬</b>", reply_markup=InlineKeyboardMarkup(buttons))
        else:
            await message.reply_photo(photo=FILTER_PIC, caption=f"<b>Total Files:</b><code>{len(files)}</code>\n<b>Movie Name:</b> <code>{search}</code>\n\n<b>© 𝐐𝐮𝐚𝐥𝐢𝐭𝐲 𝐌𝐨𝐭𝐢𝐨𝐧 𝐏𝐢𝐜𝐭𝐮𝐫𝐞𝐬</b>", reply_markup=InlineKeyboardMarkup(buttons))

    
def get_size(size):
    """Get size in readable format"""

    units = ["Bytes", "KB", "MB", "GB", "TB", "PB", "EB"]
    size = float(size)
    i = 0
    while size >= 1024.0 and i < len(units):
        i += 1
        size /= 1024.0
    return "%.2f %s" % (size, units[i])

def split_list(l, n):
    for i in range(0, len(l), n):
        yield l[i:i + n]          



@Client.on_callback_query()
async def cb_handler(client: Client, query: CallbackQuery):
    clicked = query.from_user.id
    try:
        typed = query.message.reply_to_message.from_user.id
    except:
        typed = query.from_user.id
        pass
    if (clicked == typed):

        if query.data.startswith("next"):
            ident, index, keyword = query.data.split("_")
            try:
                data = BUTTONS[keyword]
            except KeyError:
                await query.answer("You are using this for one of my old message, please send the request again.",show_alert=True)
                return

            if int(index) == int(data["total"]) - 2:
                buttons = data['buttons'][int(index)+1].copy()

                buttons.append(
                    [InlineKeyboardButton("⏪ BACK", callback_data=f"back_{int(index)+1}_{keyword}")]
                )
                buttons.append(
                    [InlineKeyboardButton(f"📃 Pages {int(index)+2}/{data['total']}", callback_data="pages")]
                )
            #    buttons.append(
                  #  [InlineKeyboardButton("✨️𝐒𝐞𝐫𝐢𝐞𝐬 𝐒𝐭𝐮𝐝𝐢𝐨✨️", url="https://t.me/Series_Studio")]
              #  )

                await query.edit_message_reply_markup( 
                    reply_markup=InlineKeyboardMarkup(buttons)
                )
                return
            else:
                buttons = data['buttons'][int(index)+1].copy()

                buttons.append(
                    [InlineKeyboardButton("⏪ BACK", callback_data=f"back_{int(index)+1}_{keyword}"),InlineKeyboardButton("NEXT ⏩", callback_data=f"next_{int(index)+1}_{keyword}")]
                )
                buttons.append(
                    [InlineKeyboardButton(f"📃 Pages {int(index)+2}/{data['total']}", callback_data="pages")]
                )
              #  buttons.append(
                  #  [InlineKeyboardButton("✨️𝐒𝐞𝐫𝐢𝐞𝐬 𝐒𝐭𝐮𝐝𝐢𝐨✨️", url="https://t.me/Series_Studio")]
             #   )

                await query.edit_message_reply_markup( 
                    reply_markup=InlineKeyboardMarkup(buttons)
                )
                return


        elif query.data.startswith("back"):
            ident, index, keyword = query.data.split("_")
            try:
                data = BUTTONS[keyword]
            except KeyError:
                await query.answer("You are using this for one of my old message, please send the request again.",show_alert=True)
                return

            if int(index) == 1:
                buttons = data['buttons'][int(index)-1].copy()

                buttons.append(
                    [InlineKeyboardButton("NEXT ⏩", callback_data=f"next_{int(index)-1}_{keyword}")]
                )
                buttons.append(
                    [InlineKeyboardButton(f"📃 Pages {int(index)}/{data['total']}", callback_data="pages")]
                )
             #   buttons.append(
                  #  [InlineKeyboardButton("✨️𝐒𝐞𝐫𝐢𝐞𝐬 𝐒𝐭𝐮𝐝𝐢𝐨✨️", url="https://t.me/Series_Studio")]
             #   )

                await query.edit_message_reply_markup( 
                    reply_markup=InlineKeyboardMarkup(buttons)
                )
                return   
            else:
                buttons = data['buttons'][int(index)-1].copy()

                buttons.append(
                    [InlineKeyboardButton("⏪ BACK", callback_data=f"back_{int(index)-1}_{keyword}"),InlineKeyboardButton("NEXT ⏩", callback_data=f"next_{int(index)-1}_{keyword}")]
                )
                buttons.append(
                    [InlineKeyboardButton(f"📃 Pages {int(index)}/{data['total']}", callback_data="pages")]
                )
               # buttons.append(
                    #[InlineKeyboardButton("✨️𝐒𝐞𝐫𝐢𝐞𝐬 𝐒𝐭𝐮𝐝𝐢𝐨✨️", url="https://t.me/Series_Studio")]
              #  )

                await query.edit_message_reply_markup( 
                    reply_markup=InlineKeyboardMarkup(buttons)
                )
                return
        elif query.data == "about":
            buttons = [
                [
                    InlineKeyboardButton('Update Channel', url='https://t.me/subin_works'),
                    InlineKeyboardButton('Source Code', url='https://github.com/subinps/Media-Search-bot')
                ]
                ]
            await query.message.edit(text="<b>Developer : <a href='https://t.me/subinps_bot'>SUBIN</a>\nLanguage : <code>Python3</code>\nLibrary : <a href='https://docs.pyrogram.org/'>Pyrogram asyncio</a>\nSource Code : <a href='https://github.com/subinps/Media-Search-bot'>Click here</a>\nUpdate Channel : <a href='https://t.me/subin_works'>XTZ Bots</a> </b>", reply_markup=InlineKeyboardMarkup(buttons), disable_web_page_preview=True)



        elif query.data.startswith("subinps"):
            ident, file_id = query.data.split("#")
            filedetails = await get_file_details(file_id)
            for files in filedetails:
                title = files.file_name
                size=files.file_size
                f_caption=files.caption
                if CUSTOM_FILE_CAPTION:
                    try:
                        f_caption=CUSTOM_FILE_CAPTION.format(file_name=title, file_size=size, file_caption=f_caption)
                    except Exception as e:
                        print(e)
                        f_caption=f_caption
                if f_caption is None:
                    f_caption = f"{files.file_name}"
                buttons = [
                    [
                        InlineKeyboardButton('🙃Channel🙃', url=f"{MAIN_LINK}")
                    ]
                    ]

                if AUTH_CHANNEL and not await is_subscribed(client, query):
                    await client.send_message(
                        chat_id=query.from_user.id,
                        text=f"**♦️ READ THIS INSTRUCTION ♦️**\n\n__🗣 നിങ്ങൾ ചോദിക്കുന്ന സിനിമകൾ നിങ്ങൾക്ക് ലഭിക്കണം എന്നുണ്ടെങ്കിൽ നിങ്ങൾ താഴെ കൊടുത്തിട്ടുള്ള ചാനലിൽ ജോയിൻ ചെയ്യണം. ജോയിൻ ചെയ്ത ശേഷം വീണ്ടും ഗ്രൂപ്പിൽ പോയി ആ ബട്ടനിൽ അമർത്തിയാൽ നിങ്ങൾക്ക് ഞാൻ ആ സിനിമ പ്രൈവറ്റ് ആയി അയച്ചു തരുന്നതാണ്..😍\n\n🗣 In Order To Get The Movie Requested By You in Our Groups, You Will Have To Join Our Official Channel First. After That, Try Accessing That Movie Again From Our Group. I'll Send You That Movie Privately 🙈__\n\n**👇 JOIN THIS CHANNEL & TRY 👇\n\n[{MAIN_LINK}]**",
                        reply_markup=InlineKeyboardMarkup(
                            [
                                [
                                    InlineKeyboardButton("💢𝙹𝚘𝚒𝚗 𝙼𝚢 𝙲𝚑𝚊𝚗𝚗𝚎𝚕💢", url=f"{MAIN_LINK}")
                                ],
                                [
                                    InlineKeyboardButton(" 🔄 𝐓𝐫𝐲 𝐀𝐠𝐚𝐢𝐧", callback_data=f"checksub#{file_id}")
                                ]
                            ]
                        ),
                        parse_mode="markdown",
                        disable_web_page_preview=True
                        )
                    return

                await client.send_cached_media(
                    chat_id=query.from_user.id,
                    file_id=file_id,
                    caption=f_caption,
                    reply_markup=InlineKeyboardMarkup(buttons)
                    )
        elif query.data.startswith("checksub"):
            if AUTH_CHANNEL and not await is_subscribed(client, query):
                await query.answer("പോയി ചാനൽ സബ്സ്ക്രൈബ് ചെയ്യടാ മോനെ🙃😎\n\nSubscribe our channel dude 🙈",show_alert=True)
                return
            ident, file_id = query.data.split("#")
            filedetails = await get_file_details(file_id)
            for files in filedetails:
                title = files.file_name
                size=files.file_size
                f_caption=files.caption
                if CUSTOM_FILE_CAPTION:
                    try:
                        f_caption=CUSTOM_FILE_CAPTION.format(file_name=title, file_size=size, file_caption=f_caption)
                    except Exception as e:
                        print(e)
                        f_caption=f_caption
                if f_caption is None:
                    f_caption = f"{title}"
                buttons = [
                    [
                        InlineKeyboardButton('🙃Channel🙃', url=f"{MAIN_LINK}")
                    ]
                    ]
                
                await query.answer()
                await client.send_cached_media(
                    chat_id=query.from_user.id,
                    file_id=file_id,
                    caption=f_caption,
                    reply_markup=InlineKeyboardMarkup(buttons)
                    )


        elif query.data == "pages":
            await query.answer()
    else:
        await query.answer("കൌതുകും ലേശം കൂടുതൽ ആണല്ലേ👀",show_alert=True)
