import re
import execjs
import requests
from urllib import parse

session = requests.session()
index_url = 'https://fanyi.baidu.com/'
lang_url = 'https://fanyi.baidu.com/langdetect'
translate_api = 'https://fanyi.baidu.com/v2transapi'
headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/106.0.0.0 Safari/537.36 Edg/106.0.1370.37'
        }

tar_lang=input('请输入目标语言：zh/en/jp/ru/de/fra/kor/::')
query = input('请输入要翻译的文字：')
# print(tar_lang,query)
session.get(url=index_url, headers=headers)
# print(session.cookies.get_dict())
response_index = session.get(url=index_url, headers=headers)
# print(response_index)
token = re.findall(r"token: '([0-9a-z]+)'", response_index.text)[0]
gtk = re.findall(r'gtk = "(.*?)"', response_index.text)[0]
print("token:"+token)
print("gtk:"+gtk)
response_lang = session.post(url=lang_url, headers=headers, data={'query': query})
lang = response_lang.json()['lan']
print("src_lang:"+lang)

with open('self1.js', 'r', encoding='utf-8') as f:
    baidu_js = f.read()
sign = execjs.compile(baidu_js).call('e', query)
print("sigh:"+sign)
translate_url = 'https://fanyi.baidu.com/#%s/zh/%s' % (lang, parse.quote(query))
acs_token = execjs.compile(baidu_js).call('ascToken', translate_url)

data={
	"from":lang,
	"to": tar_lang,
	"query": query,
	"transtype": "translang",
	"simple_means_flag": "3",
	"sign": sign,
	"token": token,
	"domain": "common",
}

headers["Acs-Token"] = acs_token

response = session.post(url=translate_api, headers=headers, data=data)
result = response.json()['trans_result']['data'][0]['dst']
print("\nresult:"+result)