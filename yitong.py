import requests
from bs4 import BeautifulSoup


class YiTong:
	def __init__(self, url):
		self.url = url
		self.session = requests.session()
		self.login_url = url+"default%E5%BF%8F%E6%BA%B4%E9%AA%81%E6%A0%9D%E7%89%9D%E7%AF%9D%E8%B2%8A.aspx"
		code = self.session.get(self.url + "CheckCode.aspx").content
		with open("H:/yzm.jpg", "wb") as f:
			f.write(code)
		self.yzm = input("请输入验证码：")

	def login(self):
		html = requests.get(self.login_url).text
		soup = BeautifulSoup(html, "lxml")
		viewstate = soup.find_all(attrs={"name": "__VIEWSTATE"})[0].get("value")
		data = {
			"__VIEWSTATE": viewstate,
			"txtUserName": "账号",
			"TextBox2": "密码",
			"txtSecretCode": self.yzm,
			'Button1': ''
		}
		home = self.session.post(self.login_url, data=data).text
		return home

	def get_course(self):
		headers = {
			"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) "
						  "Chrome/61.0.3163.100 Safari/537.36",
			"Referer": "http://222.179.134.225:81/xskbcx.aspx?xh=2014210260&xm=%C0%EE%D1%C5%B5%E4&gnmkdm=N121602"
		}
		html = self.login()
		soup = BeautifulSoup(html, "lxml")
		course_html = soup.select(".nav .top")[5]
		course_url = self.url+course_html.select("ul li a", limit=1)[0].get("href")
		html1 = self.session.get(course_url, headers=headers).text
		return html1


url = "http://222.179.134.225:81/"
L = YiTong(url)
html = L.get_course()
soup = BeautifulSoup(html, "lxml")
print(soup)