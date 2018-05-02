# https://github.com/barseghyanartur/tld
# -*-coding: utf8 -*-
from tld import get_tld


def extract_main_url(urls):
    res = None
    for i in urls:
        cur = get_tld(i, fail_silently=True)
        if cur:
            res = cur
    return res

a = extract_main_url('https://github.com/724686158/mi')
print(a)