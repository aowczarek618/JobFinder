import re

import requests
from bs4 import BeautifulSoup

HEADERS = {
    'User-Agent': "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/81.0.4044.113 Safari/537.36"}


def job_search(location, technology):
    """Method to look for a job in the Internet."""
    page_number = 1
    job_links = set()
    job_links_quantity = len(job_links)

    while True:
        nofluffjobs_url = f"https://nofluffjobs.com/pl/jobs/{location}/{technology}?criteria=city%3D{location}%20{technology}&page={page_number}"

        page = requests.get(nofluffjobs_url, headers=HEADERS)
        soup = BeautifulSoup(page.content, 'html.parser')
        for a in soup.findAll('a', class_=re.compile("^posting-list-item posting-list-item--"),
                              href=True):
            job_links.add(f"https://nofluffjobs.com{a['href']}")
        if job_links_quantity == len(job_links):
            break
        job_links_quantity = len(job_links)
        page_number += 1

    justjoin_api_url = 'https://justjoin.it/api/offers'
    page = requests.get(justjoin_api_url, headers=HEADERS)
    justjoin_job_offers = page.json()
    for job_offer in justjoin_job_offers:
        if job_offer['city'] == location and job_offer['marker_icon'] == technology:
            job_links.add(justjoin_make_job_link(job_offer["title"], job_offer['company_name'],
                                                 job_offer['city']))

    return job_links


def remove_accents(input_text):
    """
    Function useful for web scraping.
    Zażółć gęślą jaźń --> Zazolc gesla jazn
    """
    strange = 'ŮôῡΒძěἊἦëĐᾇόἶἧзвŅῑἼźἓŉἐÿἈΌἢὶЁϋυŕŽŎŃğûλВὦėἜŤŨîᾪĝžἙâᾣÚκὔჯᾏᾢĠфĞὝŲŊŁČῐЙῤŌὭŏყἀхῦЧĎὍОуνἱῺèᾒῘᾘὨШūლἚύсÁóĒἍŷöὄЗὤἥბĔõὅῥŋБщἝξĢюᾫაπჟῸდΓÕűřἅгἰშΨńģὌΥÒᾬÏἴქὀῖὣᾙῶŠὟὁἵÖἕΕῨčᾈķЭτἻůᾕἫжΩᾶŇᾁἣჩαἄἹΖеУŹἃἠᾞåᾄГΠКíōĪὮϊὂᾱიżŦИὙἮὖÛĮἳφᾖἋΎΰῩŚἷРῈĲἁéὃσňİΙῠΚĸὛΪᾝᾯψÄᾭêὠÀღЫĩĈμΆᾌἨÑἑïოĵÃŒŸζჭᾼőΣŻçųøΤΑËņĭῙŘАдὗპŰἤცᾓήἯΐÎეὊὼΘЖᾜὢĚἩħĂыῳὧďТΗἺĬὰὡὬὫÇЩᾧñῢĻᾅÆßшδòÂчῌᾃΉᾑΦÍīМƒÜἒĴἿťᾴĶÊΊȘῃΟúχΔὋŴćŔῴῆЦЮΝΛῪŢὯнῬũãáἽĕᾗნᾳἆᾥйᾡὒსᾎĆрĀüСὕÅýფᾺῲšŵкἎἇὑЛვёἂΏθĘэᾋΧĉᾐĤὐὴιăąäὺÈФĺῇἘſგŜæῼῄĊἏØÉПяწДĿᾮἭĜХῂᾦωთĦлðὩზკίᾂᾆἪпἸиᾠώᾀŪāоÙἉἾρаđἌΞļÔβĖÝᾔĨНŀęᾤÓцЕĽŞὈÞუтΈέıàᾍἛśìŶŬȚĳῧῊᾟάεŖᾨᾉςΡმᾊᾸįᾚὥηᾛġÐὓłγľмþᾹἲἔбċῗჰხοἬŗŐἡὲῷῚΫŭᾩὸùᾷĹēრЯĄὉὪῒᾲΜᾰÌœĥტ'

    ascii_replacements = 'UoyBdeAieDaoiiZVNiIzeneyAOiiEyyrZONgulVoeETUiOgzEaoUkyjAoGFGYUNLCiIrOOoqaKyCDOOUniOeiIIOSulEySAoEAyooZoibEoornBSEkGYOapzOdGOuraGisPngOYOOIikoioIoSYoiOeEYcAkEtIuiIZOaNaicaaIZEUZaiIaaGPKioIOioaizTIYIyUIifiAYyYSiREIaeosnIIyKkYIIOpAOeoAgYiCmAAINeiojAOYzcAoSZcuoTAEniIRADypUitiiIiIeOoTZIoEIhAYoodTIIIaoOOCSonyKaAsSdoACIaIiFIiMfUeJItaKEISiOuxDOWcRoiTYNLYTONRuaaIeinaaoIoysACRAuSyAypAoswKAayLvEaOtEEAXciHyiiaaayEFliEsgSaOiCAOEPYtDKOIGKiootHLdOzkiaaIPIIooaUaOUAIrAdAKlObEYiINleoOTEKSOTuTEeiaAEsiYUTiyIIaeROAsRmAAiIoiIgDylglMtAieBcihkoIrOieoIYuOouaKerYAOOiaMaIoht'

    translator = str.maketrans(strange, ascii_replacements)

    return input_text.translate(translator)


def justjoin_make_job_link(title, company, location):
    """
    Create job link from job title, company which announced job offer
    and job location for justjoin.it website.
    """

    company_url = '-'.join(company.lower().split(' '))
    title_url = re.sub(r'[\(\)]', '', '-'.join(title.lower().split(' ')))
    title_url = re.sub(r'/', '-', title_url)
    location_url = remove_accents(location.lower())

    justjoin_url = f"https://justjoin.it/offers/{company_url}-{title_url}-{location_url}"
    justjoin_api_url = f"https://justjoin.it/api/offers/{company_url}-{title_url}-{location_url}"

    page = requests.get(justjoin_api_url, headers=HEADERS)
    if page.status_code == 200:
        return justjoin_url
    return f"https://justjoin.it/offers/{company_url}-{title_url}"


def write_job_links_to_file(filename, job_links):
    """Write job links to the file."""
    with open(filename, 'w') as file:
        for job_link in job_links:
            file.write(f"{job_link}\n")


def read_job_links_from_file(filename):
    """Read job links from the file."""
    job_links = set()
    with open(filename, 'r') as file:
        for line in file:
            job_links.add(line.rstrip())

    return job_links
