from bs4 import BeautifulSoup
import requests


def print_hi(name):
    # Use a breakpoint in the code line below to debug your script.
    print(f'Hi, {name}')  # Press ⌘F8 to toggle the breakpoint.


# Press the green button in the gutter to run the script.
if __name__ == '__main__':
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/70.0.3538.102 Safari/537.36 Edge/18.19582"
    }

    params = {
        "q": "child tax credit",
        "hl": "en",
        "tbm": "nws",
    }

    response = requests.get("https://www.google.com/search", headers=headers, params=params)
    soup = BeautifulSoup(response.text, 'html.parser')

    article_urls = []
    links = soup.findAll('a')
    for link in links:
        if '/url' in link['href']:
            url = link['href']
            article_urls.append(url)
    links = [link['href'] for link in links if '/url' in link]
    print(article_urls)



    for result in soup.select('.dbsr')[:10]:
        title = result.select_one('.nDgy9d').text
        link = result.a['href']
        source = result.select_one('.WF4CUc').text
        snippet = result.select_one('.Y3v8qd').text
        date_published = result.select_one('.WG9SHc span').text
        print(f'{title}\n{link}\n{snippet}\n{date_published}\n{source}\n')

