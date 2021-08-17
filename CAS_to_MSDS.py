from bs4 import BeautifulSoup
import requests
import re

class MSDS:
    def __init__(self, cas_no, log_print=False):
        self.cas_no = cas_no
        self.msds_id = None
        self.chem_name = None
        self.log_print = log_print
        pass

    def get_msds_id(self):
        url = f'https://msds.kosha.or.kr/MSDSInfo/kcic/msdssearchAll.do'
        params = {
            'listType': 'all',
            'searchKeyword': cas_no
        }

        # parsing
        res = requests.get(url, params=params)
        soup = BeautifulSoup(res.text, 'html.parser')
        m = soup.select('div.BoardArea > table.Tbl2 > tbody > tr > td > a')
        javascript = m[0]['href']
        mat = re.search("'msds','(\d+)'", javascript)

        self.msds_id = mat.group(1)
        self.chem_name = m[0].text.strip()

        if self.log_print:
            print(self.msds_id, self.chem_name, sep='\t')






    def get_pdf(self):
        url = 'https://msds.kosha.or.kr/MSDSInfo/AIViewer/msdsAireport/msds/A_SingleMsds.jsp'
        headers = {
            'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9',
            'Accept-Encoding': 'gzip, deflate, br',
            'Accept-Language': 'ko,en-US;q=0.9,en;q=0.8',
            'Cache-Control': 'no-cache',
            'Connection': 'keep-alive',
            'Content-Type': 'application/x-www-form-urlencoded',
            'DNT': '1',
            'Host': 'msds.kosha.or.kr',
            'Origin': 'http://msds.kosha.or.kr',
            'Referer': 'http://msds.kosha.or.kr/msds/web/kosha/comform/MsdsSelectPrint.jsp?mode=A_SingleMsds&sArgMode=PDF',
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/92.0.4515.131 Safari/537.36'}
        data = {'reportMode': 'HTML',
                'menu': 'old',
                'clientURIEncoding': 'UTF-8',
                'sPrintDiv': '1111111111111111',
                'sArgChemId': self.msds_id,
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

        file_name = cas_no
        if cas_no and self.chem_name:
            file_name = f'[{cas_no}]{self.chem_name}'

        with open(f'{file_name}.pdf', 'wb') as pdf:
            pdf.write(res.content)
        print(f'{cas_no} 다운로드 완료')

        pass




cas_no_list = """64-19-7
67-64-1
75-05-8""".splitlines()


for cas_no in set(cas_no_list):
    try:
        a = MSDS(cas_no=cas_no)
        a.get_msds_id()
        a.get_pdf()
    except:
        print(cas_no, 'Fail')
