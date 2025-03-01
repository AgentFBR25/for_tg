
import asyncio
from aiogram import Bot, Dispatcher, types

import os
from aiogram.types import Message, CallbackQuery
from aiogram import F
from aiogram.filters import Command


#from aiogram.utils import executor   # для парсера
#import requests                      # для парсера
from bs4 import BeautifulSoup        # для парсера
import aiohttp                       # для парсера

import json

from aiogram.types import (
    ReplyKeyboardMarkup,
    KeyboardButton,
    InlineKeyboardMarkup,
    InlineKeyboardButton
)
from dotenv import load_dotenv





load_dotenv()
bot = Bot(os.getenv("TOKEN"))

dp = Dispatcher()
"""=============================================================================================="""



@dp.message(Command("start"))
async def command_start(message: Message):
    await message.answer(f"Привіт {message.from_user.full_name}!", reply_markup=key_shkoda)



@dp.message(F.text == "Search Shkoda")
async def pars_scoda(message: Message):
    url = "https://auto.ria.com/uk/legkovie/skoda/rapid/?page=1"
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64)"
    }

    shkoda = []
    if os.path.exists("first_test/Шкода.json"):

        with open ("first_test/Шкода.json", "r", encoding="utf-8") as file:
            data_shcoda = json.load(file)

        async with aiohttp.ClientSession() as session:
            async with session.get(url, headers=headers) as response:
                html = await response.text()
                soup = BeautifulSoup(html, "lxml")

                cars = soup.find("div", class_="standart-view").find_all("div", class_="item ticket-title")[0:5]
                cars_1 = soup.find("div", class_="standart-view").find_all("div", class_="price-ticket")[0:5]
                cars_2 = soup.find("div", class_="standart-view").find_all("div", class_="head-ticket")[0:5]

                for c, c_1, f in zip(cars, cars_1, cars_2):
                    c = c.find("a").get("href")
                    b = f.find("a").get("title")
                    k = c_1.text.strip()
                    shkoda.append({
                        "Ціна": k,
                        "Назва": b,
                        "Посилання": c
                    })
                    #await message.answer(f"{b} \n{k} \n{c}")


        old_data = {x["Назва"] + x["Посилання"]: x["Ціна"] for x in data_shcoda }  #створюю словник, де ключ буде складатись з назви + посилання, а значення буде ціна

        for car in shkoda: # створюю новий словник з нового списку, де ключ також буде назва + посиланн, значення буде ціна
            key = car["Назва"] + car["Посилання"]
            new_price = car["Ціна"]

            if key in old_data:  #  якщо ключ (назва + ціна) є в старих записах, то переходимо до порівняння ціни
                old_price = old_data[key]  # визначаю стару ціну в змінну
                if old_price != new_price: # порівнюю ціни
                    await message.answer(f"У автомобіля {key}, нова ціна {new_price}")

            else:  # якщо новго ключа (назва + посилання) не знайдено в старих записах, то додалось нове авто.
                await message.answer(f"Додано нове авто! {key} \n {new_price}")

    else:


            async with aiohttp.ClientSession() as session:
                async with session.get(url, headers=headers) as response:
                    html = await response.text()
                    soup = BeautifulSoup(html, "lxml")

                    cars = soup.find("div", class_="standart-view").find_all("div", class_="item ticket-title")[0:5]
                    cars_1 = soup.find("div", class_="standart-view").find_all("div", class_="price-ticket")[0:5]
                    cars_2 = soup.find("div", class_="standart-view").find_all("div", class_="head-ticket")[0:5]

                    for c, c_1, f in zip(cars, cars_1, cars_2):
                        c = c.find("a").get("href")
                        b = f.find("a").get("title")
                        k = c_1.text.strip()
                        shkoda.append({
                            "Ціна": k,
                            "Назва": b,
                            "Посилання": c
                        })
                        await message.answer(f"{b} \n{k} \n{c}")

    with open ("first_test/Шкода.json", "w", encoding="utf-8") as file:
            json.dump(shkoda, file, indent=4, ensure_ascii=False)




@dp.message(F.text == "Search mac Yellow")
async def search_yellow(message: Message):
    url = "https://yellow.ua/ua/apple/macbooks/hdd:256_gb;memory_ram:8_gb;model:macbook_air;processor_filtereble:apple_m1/"
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64)"
    }
    mac_yellow = []

    async with aiohttp.ClientSession() as session:
        async with session.get(url, headers=headers) as response:
            html = await response.text()
            soup = BeautifulSoup(html, "lxml")

            mac_all = soup.find("ul", class_="products-grid category-products-grid product-items-list").find_all("div", class_="product-name")
            mac_price = soup.find("ul", class_="products-grid category-products-grid product-items-list").find_all("span", class_="price")
            for mac, price in zip(mac_all, mac_price):
                mac_title = mac.find("a").get("title")
                mac_linc = mac.find("a").get("href")
                pr = price.text.strip()
                i = pr.replace("\xa0", "") # в блоці ціна замість пробілу використовуєтсья \xa0 тому я його замінюю
                text = {"Назва": mac_title,
                        "Ціна": i,
                        "Посилання": mac_linc
                }
                mac_yellow.append(text)
                await message.answer(f"{mac_title} \n\n {i} \n\n {mac_linc}")

    with open("first_test/Mac Yellow.json", "w", encoding="utf-8") as file:
        json.dump(mac_yellow, file, indent=4, ensure_ascii=False)

@dp.message(F.text == "Search mac Touch")
async def search_touch(message: Message):
    url = "https://jabko.ua/mac/macbook-air/mfp/4-ob-m-pam-yat,256gb/71-operativna-pam-yat,8gb/70-protsesor,apple-m1"
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64)"
    }
    mac_touch = []

    async with aiohttp.ClientSession() as session:
        async with session.get(url, headers=headers) as response:
            html = await response.text()
            soup = BeautifulSoup(html, "lxml")

            mac_all = soup.find("div", class_="product_catalog_").find_all("div", class_="catalog-product-item")
            for mac in mac_all:
                mc_title = mac.find("a", {"data-list": "Каталог товаров"}).get("data-name")
                mc_link = mac.find("a", {"data-list": "Каталог товаров"}).get("href")
                mc_price = mac.find("a", {"data-list": "Каталог товаров"}).get("data-price")

                mac_touch.append(
                    {
                        "Назва": mc_title,
                        "Ціна": f"{mc_price} грн",
                        "Посилання": mc_link
                    }
                )
                await message.answer(f"{mc_title} \n\n {mc_price} грн\n\n {mc_link}")

    with open ("first_test/Mac_touch.json", "w", encoding="utf-8") as file:
        json.dump(mac_touch, file, indent=4, ensure_ascii=False)


"""==============================KEYBOARD==================================="""


key_shkoda = ReplyKeyboardMarkup(
     keyboard=[
         [KeyboardButton(text="Search Shkoda")],
         [KeyboardButton(text="Search mac Yellow"), KeyboardButton(text="Search mac Touch")]
     ],
     resize_keyboard=True
 )




async def main():
    #await bot.delete_webhook(drop_pending_updates=True)
    print("Бот запущено")
    await dp.start_polling(bot)

if __name__ == '__main__':
    asyncio.run(main())