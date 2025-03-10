options = Options()
options.headless = True
driver = webdriver.Firefox(options=options)

url = "https://www.football365.com/liverpool/news"
driver.get(url)
html = driver.page_source
driver.quit()

soup = BeautifulSoup(html, 'html.parser')
pretty_html = soup.prettify()

with open("football365_liverpool.html", "w", encoding="utf-8") as file:
    file.write(pretty_html)
