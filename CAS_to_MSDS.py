from bs4 import BeautifulSoup
import requests
import re


def get_msds_id(cas_no, log_print=True):
    url = f'http://msds.kosha.or.kr/kcic/msdssearchAll.do?listType=all&searchKeyword={cas_no}'
    res = requests.get(url)

    soup = BeautifulSoup(res.text, 'html.parser')
    m = soup.find('div', {'class': 'BoardArea'}).find('table', {'class': 'Tbl2'}).find('tbody').find('td',{'class': ""})

    msds_id = re.search("'msds','(\d+)'", m.a['href']).group(1).strip()
    chem_name = m.text.strip()

    if log_print:
        print([msds_id, chem_name])

    return {'msds_id': msds_id,
            'chem_name': chem_name,
            }


def get_pdf(msds_id, cas_no=None, chem_name=None):
    url = 'http://msds.kosha.or.kr/AIViewer/msdsAireport/msds/A_SingleMsds.jsp'
    headers = {
        'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9',
        'Accept-Encoding': 'gzip, deflate',
        'Accept-Language': 'ko,en-US;q=0.9,en;q=0.8',
        'Cache-Control': 'no-cache',
        'Connection': 'keep-alive',
        'Content-Type': 'application/x-www-form-urlencoded',
        'DNT': '1',
        'Host': 'msds.kosha.or.kr',
        'Origin': 'http://msds.kosha.or.kr',
        'Referer': 'http://msds.kosha.or.kr/msds/web/kosha/comform/MsdsSelectPrint.jsp?mode=A_SingleMsds&sArgMode=PDF',
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/84.0.4147.125 Safari/537.36'}
    data = {'reportMode': 'HTML',
            'menu': 'old',
            'clientURIEncoding': 'UTF-8',
            'sPrintDiv': '1111111111111111',
            'sArgChemId': msds_id,
            'sArgChemDiv': '',
            'sArgUserId': '',
            'sArgProductId': '0',
            'sArgProductDiv': '',
            'sArgState': 'C',
            'reportParams': 'showHwp:false,showExcel:false'}

    res = requests.post(url, headers=headers, data=data)
    AIcipher = re.search('var callParameter = { \"AICipher\":\"(.*?)\"', res.text).group(1)

    data = {'AICipher': AIcipher,
            'url': 'http://msds.kosha.or.kr/AIViewer/msdsAireport/msds/A_SingleMsds.jsp'}

    res = requests.post(url, headers=headers, data=data)

    file_name = "no_name"
    if cas_no:
        file_name = cas_no
    if cas_no and chem_name:
        file_name = f'[{cas_no}]{chem_name}'

    with open(f'{file_name}.pdf', 'wb') as pdf:
        pdf.write(res.content)
    print(f'{cas_no} 다운로드 완료')


cas_no = '1185-57-5'

d = get_msds_id(cas_no)
get_pdf(d['msds_id'], cas_no=cas_no, chem_name=d['chem_name'])
get_pdf(d['msds_id'], cas_no=cas_no)
