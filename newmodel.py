import numpy as np
import pandas as pd
import re
from sklearn.feature_extraction.text import HashingVectorizer
import pandas as pd
import pickle
from sklearn.ensemble import RandomForestClassifier
from collections import Counter
import itertools
import tldextract
from urllib.parse import urlparse
from tld import get_tld
import os.path

def predict(urlIn ,loaded_model):
    def getTokens(input):
        tokensBySlash = str(input.encode('utf-8')).split('/')
        allTokens = []
        for i in tokensBySlash:
            tokens = str(i).split('-')
            tokensByDot = []
            for j in range(0, len(tokens)):
                tempTokens = str(tokens[j]).split('.')
                tokentsByDot = tokensByDot + tempTokens
            allTokens = allTokens + tokens + tokensByDot
        allTokens = list(set(allTokens))
        if 'com' in allTokens:
            allTokens.remove('com')
        return allTokens

    encoder = HashingVectorizer(n_features=300, ngram_range=(1, 4), tokenizer=getTokens)
    test = encoder.fit_transform([urlIn])
    numpyArray = test.toarray()
    panda_df = pd.DataFrame(data=numpyArray[0:, 0:],
                            index=[str(i + 1)
                                   for i in range(numpyArray.shape[0])],
                            columns=['Column_' + str(i + 1)
                                     for i in range(numpyArray.shape[1])])
    data = {'url': [urlIn]}
    df = pd.DataFrame(data)

    def digit_ratio(url):
        digits = 0
        l = 0
        for i in url:
            if i.isnumeric():
                digits = digits + 1
            if i.isalpha():
                l = l + 1
        return digits / l

    def having_ip_address(url):
        match = re.search(
            '(([01]?\\d\\d?|2[0-4]\\d|25[0-5])\\.([01]?\\d\\d?|2[0-4]\\d|25[0-5])\\.([01]?\\d\\d?|2[0-4]\\d|25[0-5])\\.'
            '([01]?\\d\\d?|2[0-4]\\d|25[0-5])\\/)|'  # IPv4
            '((0x[0-9a-fA-F]{1,2})\\.(0x[0-9a-fA-F]{1,2})\\.(0x[0-9a-fA-F]{1,2})\\.(0x[0-9a-fA-F]{1,2})\\/)'  # IPv4 in hexadecimal
            '(?:[a-fA-F0-9]{1,4}:){7}[a-fA-F0-9]{1,4}', url)  # Ipv6
        if match:
            # print match.group()
            return 1
        else:
            # print 'No matching pattern found'
            return 0

    def tld_length(tld):
        try:
            if tld in ['ru', 'cn', 'surf', 'tw', 'to', 'gq', 'ml']:
                return 1
            else:
                return 0
        except:
            return -1

    def digit_count(url):
        digits = 0
        for i in url:
            if i.isnumeric():
                digits = digits + 1
        return digits

    def no_of_dir(url):
        urldir = urlparse(url).path
        return urldir.count('/')

    def no_of_embed(url):
        urldir = urlparse(url).path
        return urldir.count('//')

    def no_of_embed1(url):
        urldir = urlparse(url).path
        return urldir.count('%20')

    def spchar(url):
        urldir = urlparse(url).path
        return len(re.findall("[$&+,:;=?@#|'<>.-^*()%!]", urldir))

    df['url_length'] = df['url'].apply(lambda i: len(str(i)))

    df['url_schar'] = df['url'].apply(lambda i: len(re.findall(':|_|\?|=|&', i)))
    df['url_dtl'] = df['url'].apply(lambda i: digit_ratio(i))
    df['tld'] = df['url'].apply(lambda i: get_tld(i, fail_silently=True))
    df['tld_length'] = df['tld'].apply(lambda i: tld_length(i))
    df['use_of_ip'] = df['url'].apply(lambda i: having_ip_address(i))
    df['hostname_length'] = df['url'].apply(lambda i: len(urlparse(i).netloc))
    df['count-digits'] = df['url'].apply(lambda i: digit_count(urlparse(i).netloc))
    df['hyphen'] = df['url'].apply(lambda i: urlparse(i).netloc.count('-'))
    df['and'] = df['url'].apply(lambda i: urlparse(i).netloc.count('@'))
    df['subdomain'] = df['url'].apply(lambda i: tldextract.extract(i).subdomain.count('.'))
    df['count_dir'] = df['url'].apply(lambda i: no_of_dir(i))
    df['count_embed_domian'] = df['url'].apply(lambda i: no_of_embed(i))
    df['count_20'] = df['url'].apply(lambda i: no_of_embed1(i))
    df['count_spchar'] = df['url'].apply(lambda i: spchar(i))
    df['count_query'] = df['url'].apply(lambda i: len(urlparse(i).query))
    new_df = df.drop(['url', 'tld'], axis=1)
    new_df.reset_index(drop=True, inplace=True)
    panda_df.reset_index(drop=True, inplace=True)
    test_features = pd.concat([panda_df, new_df], axis=1)
#    classifier = XGBClassifier(tree_method='gpu_hist')
#    classifier.load_model('model_file_name.bin')
#    loaded_model = pickle.load(open('rf300_4.pki', 'rb'))
    y_predl = loaded_model.predict(test_features)
    return y_predl[0]
