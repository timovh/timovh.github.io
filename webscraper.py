from bs4 import BeautifulSoup
import requests
import csv

payload = {
    'USERNAME': '25357',
    'PASSWORD': 'welkom'
}

HINT = 'nooit'
SUBMIT = 'oefenen'
START_GAME = "1"
TYPE = ""
WHAT = "wordbase"

def getWords(curChapter=1, how='d2w', level='2'):
    with requests.session() as s:
        # info = s.post('https://wtw.bijlescontact.nl/index.php', data=payload)
        info = s.post('https://wtw.bijlescontact.nl/dashboard/?level=1', data=payload)
        pl2 = {
            'CHAPTER[]': curChapter,
            'WHAT[]': WHAT,
            'HOW': how,
            'HINT': HINT,
            'SUBMIT': SUBMIT,
            'start_game': SUBMIT,
            'level': level,
            'type': TYPE
        }
        t1 = s.post('https://wtw.bijlescontact.nl/practice/', data=pl2)
        soup = BeautifulSoup(t1.text, "html.parser")
        pos_tot = soup.find("div", id="current_word_number").text
        startandend = pos_tot.split('/')
        curItem = int(startandend[0])
        totalItems = int(startandend[1])
        curId = soup.find("input", {'name': "ID"})['value']
        pl3 = {
            'FOREIGN': "",
            'WHAT[]': WHAT,
            'HOW': how,
            'ID': curId,
            'NEXT': 'Volgende'
        }
        csvHeaders = ['question', 'answer', 'id']
        with open(f'csvFiles/chap{curChapter}.csv', 'w') as f:
            myCsv = csv.writer(f)
            myCsv.writerow(csvHeaders)
            for i in range(totalItems):
                p2 = s.post('https://wtw.bijlescontact.nl/practice/', data=pl3)
                soup2 = BeautifulSoup(p2.text, 'html.parser')
                table = soup2.find('table', class_ = 'hinttable')
                lc = table.find('td', class_='left-cell')
                rc = table.find('td', class_='right-cell')
                rc.find('audio').decompose()
                # pl3['ID'] === the id of the next item
                if curItem <= (totalItems - 1):
                    pl3['ID'] = soup2.find("input", {'name': "ID"})['value']
                question = lc.text.strip()
                answer = rc.text.strip()
                id = curItem
                csvData = [question, answer, id]
                myCsv.writerow(csvData)
                curItem += 1
