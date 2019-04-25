from bs4 import BeautifulSoup as bs
from selenium import webdriver
from selenium.webdriver.chrome.options import Options

chrome_options = Options()
chrome_options.add_argument("--headless")
chrome_options.add_argument("--window-size=1920x1080")
driver = '/path/to/chrome/webdriver'

def wri(page):
	with open('res1.html','r+') as f:
		f.write(page)
		f.close()

def get_links(base_url):
	browser = webdriver.Chrome(chrome_options=chrome_options, executable_path=driver)
	browser.get(base_url)
	sp = bs(browser.page_source, 'html.parser')
	a = sp.find_all('a', {'class':'a-link-normal a-text-normal'})
	links = []
	for items in a:
		links.append('https://www.amazon.de'+items.get('href'))
	browser.close()
	return links, sp

def read_reviews(link):
	browser = webdriver.Chrome(chrome_options=chrome_options, executable_path=driver)
	browser.get(link)
	wri(browser.page_source)
	sp = bs(browser.page_source, 'html.parser')
	rt = sp.find('span',{'id':'productTitle'}).text.strip()
	print ('Review for product: ',rt)
	see_all = sp.find('a',{'data-hook':'see-all-reviews-link-foot'})
	size = int(see_all.text.split()[1])
	divs = []
	l1 = 'https://www.amazon.de'+see_all.get('href')
	for i in range(1,size+1,10):
		browser.get(l1)
		sp2 = bs(browser.page_source,'html.parser')
		d = sp2.find_all('div',{'class':'a-section celwidget'})
		for j in d:
			divs.append(j)
		li = sp2.find('li',{'class':'a-last'})
		if li:
			try:
				a = li.find('a')
				l1 = 'https://www.amazon.de'+a.get('href')
			except(AttributeError):
				pass
	browser.close()
	return divs
if __name__ == '__main__':
	base_url = 'https://www.amazon.de/s?k=hundedecke+auto&__mk_de_DE=%C3%85M%C3%85%C5%BD%C3%95%C3%91&ref=nb_sb_noss_2'
	while True:
		links, sp = get_links(base_url)
		for i in links:
			divs = read_reviews(i)
			for item in divs:
				print('Review by: ',item.find('span',{'class':'a-profile-name'}).text.strip())
				print('Review Title: ',item.find('a',{'data-hook':'review-title'}).text.strip())
				print('Review Text: ',item.find('span',{'data-hook':'review-body'}).text.strip())
		li = sp.find('li',{'class':'a-last'})
		if li:
			try:
				a = li.find('a')
				base_url = 'https://www.amazon.de'+a.get('href')
			except(AttributeError):
				break

