from base.module import command, BaseModule
from pyrogram.types import Message
import requests 
import random as r

class ExchangeRate(BaseModule):
    VALUTES = {
        "руб": "RUB",
        "₽": "RUB",
        "грн": "UAH",
        "₴": "UAH",
        "₸": "KZT",
        "pl": "PLN",
        "zl": "PLN",
        "zł": "PLN",
        "$": "USD",

    }

    @command("exrate")
    async def handle_val_command(self, _, message: Message):
        """{quantity} [currency]"""
        emt = self.S["err"]["empty"]
        valut = self.S["err"]["val"]
        inpt = self.S["err"]["inp"]
        args = message.text.split(maxsplit=1)
        if len(args) < 2:
            await message.reply(emt)
            return
        args = args[1].strip()
        tray = "" # default value
        if args:
            tray = args
        args_list = args.split(" ")
        try:
            if len(args_list) == 1 and isinstance(float(args_list[0]), float) == True:
                args_list.append(str(tray))
        except Exception:
            args_list = ["1", args_list[0]]
        currency = args_list[1].lower()  # convert to lowercase

        # check if currency is in the VALUTES dictionary, and get the corresponding code
        if currency in self.VALUTES:
            currency = self.VALUTES[currency]

        api = requests.get(
            f"https://min-api.cryptocompare.com/data/price?fsym={currency}&tsyms=USD,RUB,UAH,PLN,KZT,BTC,ETH,TONCOIN"
        ).json()
        try:
            try:
                quantity = float(args_list[0])
                result = (
                    "👌 <b>{} {} is:</b>\n\n"
                    " 🇺🇦"
                    " <code>{}₴</code>\n"
                    " 🇺🇸"
                    " <code>{}$</code>\n"
                    " 🇵🇱"
                    " <code>{}zł</code>\n"
                    " 🇰🇿"
                    " <code>{}₸</code>\n"
                    " 🇷🇺"
                    " <code>{}₽</code>\n"
                    " 💰 <code>{}"
                    " ETH</code>\n 🪙"
                    " <code>{} BTC</code>\n"
                    " 💸 <code>{} TONCOIN</code>"
                ).format(
                    quantity,
                    currency,
                    round(api["UAH"] * quantity, 2),
                    round(api["USD"] * quantity, 2),
                    round(api["PLN"] * quantity, 2),
                    round(api["KZT"] * quantity, 2),
                    round(api["RUB"] * quantity, 2),
                    round(api["ETH"] * quantity, 4),
                    round(api["BTC"] * quantity, 4),
                    round(api["TONCOIN"] * quantity, 4),
                )
                await message.reply(result)
            except KeyError:
                await message.reply(valut)
        except ValueError:
            await message.reply(inpt)
