from bs4 import BeautifulSoup
import requests
import datetime
from oauth2client.service_account import ServiceAccountCredentials
import gspread


def create_rows(soup):
    today = datetime.datetime.today()
    rows = []

    links = soup.find_all('a')
    for link in links:
        if '/url' in link['href'] and 'google' not in link['href']:
            if link.next_element.name == 'h3':      # there are some duplicates, ones with h3 after are the ones with title etc.
                url = link['href']
                url = url.split('/&amp')[0].split('&sa')[0].lstrip('/url?q=')    # remove google generated garbage at the end
                title = link.next_element.text
                publisher = link.next_element.next_sibling.text
                hf_mentioned = is_hf_mentioned(url)
                rows.append([title, 'subtitle', today, publisher, 'author', url, hf_mentioned])
    return rows


def is_hf_mentioned(url):
    response = requests.get(url)
    soup = BeautifulSoup(response.text, 'html.parser')
    paragraphs = soup.find_all(text=True)
    humanity_forward_mentioned = False
    for paragraph in paragraphs:
        paragraph = paragraph.lower()
        if 'humanity forward' in paragraph:
            humanity_forward_mentioned = True
            break
        elif 'longer the monthly ctc payments were in place' in paragraph:
            print('yeah')
    return humanity_forward_mentioned


def write_rows_to_gsheet(rows):
    scopes = ['https://spreadsheets.google.com/feeds','https://www.googleapis.com/auth/drive']
    credentials = ServiceAccountCredentials.from_json_keyfile_name("my_email_svc_account.json",
                                                                   scopes)  # access the json key you downloaded earlier
    client = gspread.authorize(credentials)
    sheet = client.open('Test HF Sheet')

    # get the first sheet of the Spreadsheet
    sheet_instance = sheet.get_worksheet(0)
    for row in rows:
        print('appending row', row)
        sheet_instance.append_row(row)


if __name__ == '__main__':
    headers = {
        # "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/70.0.3538.102 Safari/537.36 Edge/18.19582"
    }

    params = {
        "q": "child tax credit",
        "hl": "en",
        "tbm": "nws",
    }

    response = requests.get("https://www.google.com/search", headers=headers, params=params)
    soup = BeautifulSoup(response.text, 'html.parser')

    rows = create_rows(soup)
    write_rows_to_gsheet(rows)









