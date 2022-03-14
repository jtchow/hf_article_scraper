from bs4 import BeautifulSoup
import requests
import datetime
from oauth2client.service_account import ServiceAccountCredentials
import gspread
from pprint import pprint


def log_latest_news_articles(search_term='child tax credit'):
    params = {
        "q": search_term,
        "hl": "en"
    }
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/70.0.3538.102 Safari/537.36 Edge/18.19582"
    }
    response = requests.get("https://www.news.google.com/search", headers=headers, params=params)
    soup = BeautifulSoup(response.text, 'html.parser')
    print('getting articles')

    rows = create_rows(soup)
    write_rows_to_gsheet(rows)


def create_rows(soup):
    print('processing articles')
    today = datetime.datetime.today().strftime('%Y-%m-%d')
    rows = []

    # get all the info for the whole result set
    links = soup.find_all('a', {'class': ['DY5T1d RZIKme', 'wEwyrc AVN2gc uQIVzc Sksgp']})
    # links looks like : title, publisher, title, publisher so we do below
    titles = [link.text for link in links[::2]]  # grab every other element for title
    publishers = [link.text for link in links[1::2]]  # grab every other element for publisher
    urls = []
    hf_mentions = []

    links = links[::2]          # filter links down to true links
    google_generated_extensions = [link.get('href') for link in links]
    google_generated_extensions = [url.strip('.') for url in google_generated_extensions]
    for url_extension in google_generated_extensions:
        res = requests.get('https://www.news.google.com' + url_extension)
        urls.append(res.url)
        hf_mentioned = is_hf_mentioned(res)
        hf_mentions.append(hf_mentioned)

    # put together the actual rows we are going to insert in gsheets
    for i in range(len(links)):
        title = titles[i]
        publisher = publishers[i]
        url = urls[i]
        hf_mentioned = hf_mentions[i]
        rows.append([title, 'subtitle', today, publisher, 'author', url, hf_mentioned])
    print('finished_processing articles')
    return rows


def is_hf_mentioned(response):
    soup = BeautifulSoup(response.text, 'html.parser')
    paragraphs = soup.find_all(text=True)
    humanity_forward_mentioned = False
    for paragraph in paragraphs:
        paragraph = paragraph.lower()
        if 'humanity forward' in paragraph:
            humanity_forward_mentioned = True
            break
        # # sanity check to see if text parsing was working
        # elif 'longer the monthly ctc payments were in place' in paragraph:
        #     print('yeah')
    return humanity_forward_mentioned


def write_rows_to_gsheet(rows):
    print('writing rows to google sheets')
    scopes = ['https://spreadsheets.google.com/feeds','https://www.googleapis.com/auth/drive']
    credentials = ServiceAccountCredentials.from_json_keyfile_name("my_email_svc_account.json",
                                                                   scopes)  # access the json key you downloaded earlier
    client = gspread.authorize(credentials)
    sheet = client.open('Test HF Sheet')

    sheet_instance = sheet.get_worksheet(0)
    for row in rows:
        sheet_instance.append_row(row)

    print('done!')


if __name__ == '__main__':
    search_term = 'child tax credit when:1d'
    log_latest_news_articles(search_term)

    # params = {
    #     "q": search_term,
    #     "hl": "en"
    # }
    # headers = {
    #     "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/70.0.3538.102 Safari/537.36 Edge/18.19582"
    # }
    # response = requests.get("https://www.news.google.com/search", headers=headers, params=params)
    # soup = BeautifulSoup(response.text, 'html.parser')
    # print('getting articles')
    #
    # today = datetime.datetime.today().strftime('%Y-%m-%d')
    # rows = []
    #
    # # get all the info for the whole result set
    # links = soup.find_all('a', {'class': ['DY5T1d RZIKme']})
    # # links looks like : title, publisher, title, publisher so we do below
    # titles = [link.text for link in links[::2]]  # grab every other element for title
    # publishers = [link.text for link in links[1::2]]  # grab every other element for publisher
    # urls = []
    # hf_mentions = []
    #
    # google_generated_extensions = [link.get('href') for link in links]
    # google_generated_extensions = [url.strip('.') for url in google_generated_extensions]
    # for url_extension in google_generated_extensions:
    #     res = requests.get('https://www.news.google.com' + url_extension)
    #     urls.append(res.url)
    #     hf_mentioned = is_hf_mentioned(res)
    #     hf_mentions.append(hf_mentioned)
    #
    # # put together the actual rows we are going to insert in gsheets
    # for i in range(len(links)):
    #     title = titles[i]
    #     publisher = publishers[i]
    #     url = urls[i]
    #     hf_mentioned = hf_mentions[i]
    #     rows.append([title, 'subtitle', today, publisher, 'author', url, hf_mentioned])
    # print('finished_processing articles')
    # print('writing rows to google sheets')
    # scopes = ['https://spreadsheets.google.com/feeds','https://www.googleapis.com/auth/drive']
    # credentials = ServiceAccountCredentials.from_json_keyfile_name("my_email_svc_account.json",
    #                                                                scopes)  # access the json key you downloaded earlier
    # client = gspread.authorize(credentials)
    # sheet = client.open('Test HF Sheet')
    #
    # sheet_instance = sheet.get_worksheet(0)
    # for row in rows:
    #     sheet_instance.append_row(row)














