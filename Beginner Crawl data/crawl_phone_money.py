from bs4 import BeautifulSoup
import requests

# res = requests.get('https://chosim24h.com/dinh-gia-sim.html?simdg=0916999999')
phone = '0916999999'
res = requests.get(f'https://chosim24h.com/dinh-gia-sim.html?simdg={phone}')


soup = BeautifulSoup(res.text, "lxml")
# money = soup.find("div", {"class": "box-mang-body mb-10"})
money = soup.find("div", {"style": "font-size: 22px; font-weight: bold; margin-top: 10px; color: #fff385"}).text.strip()
# print(money)

print(money[:-1])