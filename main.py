import requests
from bs4 import BeautifulSoup
import lxml
import json
import time


url = "https://www.pixiv.net/new_illust.php"
initUrl = "https://www.pixiv.net/ajax/illust/new?lastId=0&limit=200&type=illust&r18=false&lang=zh_tw"
f = "https://www.pixiv.net/ajax/illust/new?lastId="
b = "&limit=20&type=illust&r18=true&lang=zh_tw"


headers = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/88.0.4324.150 Safari/537.36",
    "Cookie": "first_visit_datetime_pc=2021-10-08+21%3A56%3A26;  yuid_b=QmaSVkU; _gcl_au=1.1.101785192.1633697787; device_token=f92dda9ae4ae09fc68cbfc939b253018; c_type=22; privacy_policy_notification=0; a_type=0; b_type=1; PHPSESSID=29948668_JNgev5mRyejVqkB9X35mQk7C4IXNy58N; privacy_policy_agreement=0; tag_view_ranking=0xsDLqCEW6~MM6RXH_rlN~tgP8r-gOe_~Ie2c51_4Sp~Lt-oEicbBr~kGYw4gQ11Z~dUhrZMpRPB~lH5YZxnbfC~HLWLeyYOUF~0j_zFcQpTM~BtXd1-LPRH~jpK92qbLEL~aenkCCpRbu~qpSL4xzMj8~kg-ao_h7VH~G7ADIqZjq3~cryvQ5p2Tx~Ged1jLxcdL~9Wtedurr6j~4QIrb8TeMy~DADQycFGB0~aFp_IhGMJo~NKaWczYEa-~nkASI67vD1~xylAw-lsa7~SWd1IFkeUs~THI8rtfzKo~_hQmHJEG0R~fknAj5Caqc~MUQoS0sfqG~3cT9FM3R6t~X1ZSbphPDx~BU9SQkS-zU~y8GNntYHsi~8p7FrLtVHU~HcBlC3F1Sy~H-R0kn6kl8~aUKGRzPd6e~kvi9TAuD-r~ZMIwqQI05A~frpwMgnK1f~jEoxuA2PIS~Kw3rxm81BS~zfe8inf2b5~VBEfuG5k7L~_EOd7bsGyl~ziiAzr_h04~DlTwYHcEzf~VRuBtwFc6O~OUF2gvwPef~Uhg1g_SJrF~KS5kY2k_1V~iWrovDEgHB~BSlt10mdnm~RTJMXD26Ak~TWrozby2UO~xha5FQn_XC~KN7uxuR89w~qcYo_5oqVP~_bee-JX46i~wOoq4sXjoA~zyKU3Q5L4C~faHcYIP1U0~5oPIfUbtd6~f-WPkHbqBj~30UTnRZA1s~-bnWSQgCG_~PHQDP-ccQD~O2wfZxfonb~RiiwngF-C5~3gc3uGrU1V~GXcsoMs4C9~qBVGbZbpq5~Yu2Ryjfj3q~lBcRAWFuPM; __cf_bm=.jR189zMXOzz2pKo.q.yiMOFnm..iVZ8EBzqLWn0HzE-1633941036-0-ASmiFC6PB1b1nJ1OKuLI+dkrAniyhyyimSWyAF7rDgo52PqILM6l4j9rbcZP4GEk5JRFqtS1VtagmXPVbStAF0wTOSCTVj7bfnlSXe7EStQJitXHY4hdmG3C3kXkfkMJHOUdyMJrvxGXnUKQyVwBKHgeINcv2qmbHouns5cKqyw68Olk/xswRsg04hqoxlldXA==;"
}

cookie = {}


def cookieFormatter(cookieJson):
    cookieStr = json.dumps(cookieJson).split(
        "{")[-1].split("}")[0].replace("\"", "").replace(",", ";").replace(":", "=").replace(" ", "")
    # print(cookieStr)
    return cookieStr


def scraper(s):
    global headers
    res = s.get(url=url, headers=headers)
    cookie = res.cookies.get_dict()
    return cookieFormatter(cookie)


def recUrl(s, lastId):
    requestUrl = f+str(lastId)+b
    # print(requestUrl)
    cc = s.get(url=requestUrl, headers=headers)
    contentJson = json.loads(cc.content)
    with open("./log.txt", "a+", encoding='UTF-8') as file:
        file.write(json.dumps(
            contentJson, ensure_ascii=False).encode("utf-8").decode() + "\n")
    print("finished: ", lastId)
    if(not contentJson["error"]):
        print("OKK")
        recUrl(s, contentJson["body"]["lastId"])
    else:
        return


def main():
    with requests.Session() as s:
        headers['Cookie'] += scraper(s)
        recUrl(s, 0)


if __name__ == '__main__':
    main()
