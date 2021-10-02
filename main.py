import requests
import json
import base64
from tkinter import messagebox
import tkinter as tk
from tkinter import ttk
import tkinter.font as tkFont
import os
import time
import sys
from pathlib import Path
from time import strptime
def handle_focus_in(event, ent):
    ent.delete(0, tk.END)
    ent.config(fg='black')
def to_upload():
	pass


path =os.path.abspath(os.curdir)+'/folders'
if Path(path).is_dir():
	pass
else:
	messagebox.showinfo("ВНИМАНИЕ!","Создайте папку 'folders' в директории с программой!")
	sys.exit(1)
print(path)
print(os.path.dirname(os.path.realpath(__file__)))
subfolders = [ f.path for f in os.scandir(os.path.abspath(os.curdir)+'/folders') if f.is_dir() ]
print (subfolders)



#СООБЩИТЬ ЗАКАЗЧИКУ ЧТО В ПЕРВОЙ СТРОЧКЕ УКАЗАТЬ HTTP OR HTTPS

	
def main():
	def to_date(x):

		month1 = strptime(x[1:4],'%b').tm_mon
		day = x[x.find(' ')+1:x.find(',')]
		year = x[x.find(',')+2:x.find( ' ',x.find(',')+2)]
		hour = x[x.find( ' ',x.find(',')+2)+1:x.find(':')]
		minutes = x[x.find(':')+1:x.find(' ',x.find(':'))]
		am_pm = x[-2]+x[-1]
		print(am_pm)
		month = str(month1)
		if len(day) == 1:
			day = '0'+day
		if len(month)== 1:
			month = '0'+month
		if am_pm == 'pm':
			hour = str(int(hour)+12)
			if len(hour) == 1:
				hour = '0'+hour
			
		if len(minutes)==1:
			minutes = '0'+minutes

		"""
				2021-09-30T18:00:00
		"""
		return year+"-"+str(month)+"-"+day+"T"+hour+":"+minutes+":00"
	def more_tags(x):
		x = x.replace(' ','')
		x = x.replace('\n','')
		return x.split(',')

	def write_to_wordpress():
		ids=[]
		if len(subfolders) > 1:
			directory = combo.get()
		else:
			directory = labelFol.get()
		files = os.listdir(directory)
		filest = files.endswith(".txt")

		for i in range(len(filest)):
			f = open(filename, 'r')
			x = f.readline()
			print(x)
			site_name_izmenit = x[0:x.find(' ')]
			site_name_without_http_s = site_name_izmenit[site_name_izmenit.rfind('/')+1:len(site_name_izmenit)]
			site_name_without_postfix_and_prefix = site_name_izmenit[site_name_izmenit.rfind('/')+1:site_name_izmenit.find('.')]

			new_site = "https://google.com"

			new_site_without_http_s = new_site[new_site.rfind('/')+1:len(new_site)]
			new_site_without_postfix_and_prefix = new_site[new_site.rfind('/')+1:new_site.find('.')]
			
			x = f.read()
			f.close()
			text = x.replace(site_name_izmenit,new_site)
			text1 = text.replace(site_name_without_http_s,new_site_without_http_s)
			text2 = text1.replace(site_name_without_postfix_and_prefix,new_site_without_postfix_and_prefix)
			mas = text2.split('----')
			x= []
			for i in mas:
				if len(i) > 4:
					x.append(i[i.find('\n'):i.rfind('\n')])

			title = x[0].replace('\n','')
			content = x[1]
			date = to_date(x[6])

			tags = more_tags(x[7])

			meta = x[5]	

			
			USER = ent_user_name.get()
			PASSWORD = ent_password.get()



			


			#загрузка картинки

			img_path = files.i

			url = ent_url+"/wp-json/wp/v2/media"
			creds = USER + ':' + PASSWORD

			token = base64.b64encode(creds.encode())

			header = {
			    'Authorization': 'Basic ' + token.decode('utf-8'),
			    "Accept": "application/json",
			}

			media = {
			    'file': open(img_path, 'rb'),
			    'caption': 'First TEST API Image upload',
			    'description': 'First TEST API Image upload'
			}

			image = requests.post(url=url, headers=header, files=media)
				

		


	root = tk.Tk()
	root.withdraw()
	connectWin = tk.Toplevel(root)
	default_font = tkFont.nametofont("TkDefaultFont")
	default_font.configure(size=18)
	root.option_add('*Font', default_font)
	connectWin.title("Posting to WordPress")
	connectWin.geometry('600x300')
	frm_form = tk.Frame(connectWin,relief=tk.SUNKEN, borderwidth=3)

	frm_form.pack(pady=15)

	lbl_user_name = tk.Label(master=frm_form, text="user:")
	ent_user_name = tk.Entry(master=frm_form, width=40,fg='grey')

	ent_user_name.bind("<FocusIn>", lambda e,ent=ent_user_name: handle_focus_in(e,ent))

	cmb_form = tk.Frame(connectWin, borderwidth=10,relief=tk.RIDGE)

	cmb_form.pack(pady=10)
	if len(subfolders) > 1:
		combo = ttk.Combobox(cmb_form, values=subfolders,width=47)
		combo.current(1)
		combo.grid(row = 1, column=1,columnspan=3)
	elif subfolders:
		labelFol = tk.Label(cmb_form, text=subfolders,width=47)
		labelFol.grid(row = 1, column=1,columnspan=3)
	else:
		messagebox.showinfo("ВНИМАНИЕ!","Нет папок для загрузки на сервер!")
		time.sleep(0.2)
		messagebox.showinfo("ВНИМАНИЕ!","Создайте каталоги в 'folders'!")
		sys.exit(1)

	ent_user_name.insert(0,"admin")

	lbl_user_name.grid(row=0, column=0, sticky="e",pady=5)
	ent_user_name.grid(row=0, column=1,pady=5)
	 

	lbl_password = tk.Label(master=frm_form, text="password:")
	ent_password = tk.Entry(master=frm_form, width=40,fg='grey', show = '*')

	ent_password.bind("<FocusIn>", lambda e, ent = ent_password: handle_focus_in(e,ent))



	lbl_password.grid(row=1, column=0, sticky="e",pady=5)
	ent_password.grid(row=1, column=1,pady=5)
	 

	lbl_url = tk.Label(master=frm_form, text="URL:")
	ent_url = tk.Entry(master=frm_form, width=40,fg='grey')
	ent_url.insert(0,"http://example123.com")

	ent_url.bind("<FocusIn>", lambda e,ent =ent_url: handle_focus_in(e,ent))



	lbl_url.grid(row=2, column=0, sticky="e",pady=5)
	ent_url.grid(row=2, column=1,pady=5)

	frm_buttons = tk.Frame(connectWin,borderwidth=5,relief= tk.RAISED)
	frm_buttons.pack(fill=tk.X,side=tk.BOTTOM, ipadx=5, ipady=5)

	btn_connect = tk.Button(master=frm_buttons, text="Сделать записи!", command=write_to_wordpress)
	btn_connect.pack(side=tk.RIGHT, padx=10, ipadx=10)




	url = "http://kima11s2.beget.tech/wp-json/wp/v2/posts"

	user = 'admin'
	password = 'cSdP 0f46 96NV hZGJ bN8V mVp1'

	credentials = user + ':' + password
	token = base64.b64encode(credentials.encode())
	header = {'Authorization': 'Basic ' + token.decode('utf-8'), "Accept": "application/json"}
	post = {
	 'keywords': 'COVID-19 pandemic',
	 'title'    : 'SITENAME_IZMENIT reduce the cost of premium access for users to the COVID-19 pandemic',
	 'status'   : 'publish',
	 #'tags':'[SITENAME_IZMENIT, SITENAME_IZMENIT.com, Bitcoin, Blockchain, Btc, Crypto, Cryptocurrencies, Cryptocurrency, Cryptocurrency Exchange, cryptoexchange, cryptotrader, cryptotrading, ETH, Ethereum, Giveaway, KYC, Trading,  BitcoinTrading, Trading Analysis, DeFi, Business Regulation, PriceSpotlight]', 
	 #'meta': 'SITENAME_IZMENIT.com company, is proud to announce the creation of the COVID-19 Pandemic Response Fund.',
	 'post_tag':['Bitcoin, Blockchain'],
	 'featured_media': 47,
	 'content'  : '''
	 <!-- wp:paragraph -->
	<p><strong>SITENAME_IZMENIT.com</strong>&nbsp;<a href="http://SITENAME_IZMENIT.com/">company</a>, is proud to announce the creation of the COVID-19 Pandemic Response Fund. They have committed&nbsp;<strong>$2.5 million</strong>&nbsp;to global efforts to combat the pandemic.</p>
	<!-- /wp:paragraph -->

	<!-- wp:paragraph -->
	<p><strong>SITENAME_IZMENIT</strong> COVID-19 Pandemic Response Fund has awarded grants ranging from $300,000 to $1 million for a total of $2.5 million and also reduced the cost of&nbsp;<strong>premium access</strong>&nbsp;to&nbsp;<strong><a href="https://SITENAME_IZMENIT.com/" target="_blank" rel="noreferrer noopener">SITENAME_IZMENIT.com</a></strong> users from the&nbsp;<strong>United States</strong>,&nbsp;<strong>Canada</strong>,&nbsp;<strong>France</strong>,&nbsp;<strong>Italy</strong>,&nbsp;<strong>Sweden</strong>&nbsp;due to the severe consequences of this disease and the inability of people to pay the full amount.</p>
	<!-- /wp:paragraph -->

	<!-- wp:paragraph -->
	<p>The COVID-19 epidemic is an unprecedented crisis that requires a coordinated response on a global scale. Business can play a critical role in slowing the spread of the virus, mitigating its effects and saving lives, and SITENAME_IZMENIT.com are committed to making their contribution.</p>
	<!-- /wp:paragraph -->

	<!-- wp:paragraph -->
	<p>We work in the financial and technological sector, and for us the best way to help a common cause is charity.</p>
	<!-- /wp:paragraph -->

	<!-- wp:paragraph -->
	<p>In the context of the current crisis, charity is of great importance; strategically targeted funds can become a lifeline in areas that are not yet covered by global assistance at the state level, and quickly expand the capabilities of organizations prepared for the crisis, but not sufficiently resourced. The four organizations we have decided to support are playing a leading role in the fight against the COVID-19 pandemic and, with more funding, can increase the scale of the response.</p>
	<!-- /wp:paragraph -->

	<!-- wp:paragraph -->
	<p>The global crisis has forced us to think about how to build up resources to better respond to the next pandemic. To cope with new epidemics, we must learn to prevent them before they begin, quickly detect them if they have not been prevented, and quickly develop countermeasures that can be deployed across the country or the world.</p>
	<!-- /wp:paragraph -->

	<!-- wp:paragraph -->
	<p>CEO and Co-founder of&nbsp;<a href="http://SITENAME_IZMENIT.com">SITENAME_IZMENIT</a>: “We take a conscious approach to providing grants and want our actions during the COVID-19 crisis to bring maximum benefit now and in the future. Therefore, we have decided to provide grants totaling $ 2.5 million to four organizations that make a tangible contribution to the fight against the COVID-19 epidemic and help mitigate global catastrophic biological risks.”</p>
	<!-- /wp:paragraph --> ''',
	 'categories': 5, # category ID
	 'date'   : '2021-09-30T18:00:00'
	 ''
	}
	responce = requests.post(url , headers=header, json=post)
	print(responce.status_code)
	root.mainloop()
main()