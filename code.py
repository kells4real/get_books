
def get_books(title, topic):
    headers = {
        'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 11_2_3) AppleWebKit/537.36 '
                      '(KHTML, like Gecko) Chrome/89.0.4389.82 Safari/537.36'
    }
    url = 'http://books.toscrape.com/'

    page = requests.get(url, headers=headers)
    index = 0
    soup = BeautifulSoup(page.content, "html.parser")
    result = soup.findAll('div', {"class": "side_categories"})
    pattern = re.compile(r'[A-Za-z]+ ?[A-Za-z]+ ?[A-Za-z]+')

    li = []

    for items in result:
        subs = items.findAll('li')
        for sub in subs:
            i = pattern.search(sub.get_text()).group(0).lower()
            index += 1
            if i == topic.lower():
                link = "-".join(i.split(" "))
                url = f'http://books.toscrape.com/catalogue/category/books/{link}_{index}/index.html'
                page = requests.get(url, headers=headers)
                soup = BeautifulSoup(page.content, "html.parser")
                pattern2 = re.compile(r'[0-9]+ of [0-9]+')
                f = soup.findAll('li', class_='current')
                if len(f) > 0:
                    path = int(pattern2.search(soup.find('li', class_='current').text).group(0)[-2:])
                    num = path
                else:
                    num = 0
                if num:
                    url = f'http://books.toscrape.com/catalogue/category/books/{link}_{index}/index.html'
                    page2 = requests.get(url, headers=headers)
                    soup2 = BeautifulSoup(page2.content, "html.parser")
                    all_books = soup2.findAll(
                        "li", {"class": "col-xs-6 col-sm-4 col-md-3 col-lg-3"})
                    for q in all_books:
                        li.append(q.h3.a['title'].lower())
                    for o in range(1, num):
                        url = f'http://books.toscrape.com/catalogue/category/books/{link}_{index}/page-{str(o+1)}.html'
                        page2 = requests.get(url, headers=headers)
                        soup2 = BeautifulSoup(page2.content, "html.parser")
                        all_books = soup2.findAll(
                            "li", {"class": "col-xs-6 col-sm-4 col-md-3 col-lg-3"})
                        for q in all_books:
                            li.append(q.h3.a['title'].lower())
                else:
                    url = f'http://books.toscrape.com/catalogue/category/books/{link}_{index}/index.html'
                    page2 = requests.get(url, headers=headers)
                    soup2 = BeautifulSoup(page2.content, "html.parser")
                    all_books = soup2.findAll(
                        "li", {"class": "col-xs-6 col-sm-4 col-md-3 col-lg-3"})
                    for q in all_books:
                        li.append(q.h3.a['title'].lower())
                if title.lower() in li:
                    return True
                else:
                    return False
