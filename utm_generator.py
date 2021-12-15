import requests
import json
import urllib.parse

# If you want use cutt.ly or vk.cc, you need insert API-keys there.
cuttly_api_key = '12345'
vkcc_api_key = '12345'

# Utm-labels for first group
terms_group1 = [{
    "utm_source": "facebook",
    "utm_term": "sosial_group1_name",
    "shorter": "clck.ru"
  }, {
    "utm_source": "vkontakte",
    "utm_term": "sosial_group1_name",
    "shorter": "vk.cc"
  }, {
    "utm_source": "linkedin",
    "utm_term": "sosial_group1_name",
    "shorter": "cutt.ly"
}]

# Utm-labels for second group
terms_group2 = [{
    "utm_source": "facebook",
    "utm_term": "sosial_group2_name",
    "shorter": "is.gd"
  }, {
    "utm_source": "vkontakte",
    "utm_term": "sosial_group2_name",
    "shorter": "cutt.ly"
  }, {
    "utm_source": "linkedin",
    "utm_term": "sosial_group2_name",
    "shorter": "is.gd"
}]

def short_link(url, shorter):
    try:

        out = ''

        if shorter == 'clck.ru':
            response = requests.get(f'https://clck.ru/--?url={urllib.parse.quote(url)}')
            out = response.text
        elif shorter == 'cutt.ly':
            response = requests.get(f'https://cutt.ly/api/api.php?key={cuttly_api_key}&short={urllib.parse.quote(url)}')
            if response.status_code != 429:
                answer = json.loads(response.text)
                out = (answer['url']['shortLink'])
            else:
                out = '[Free version of cutt.ly can shorts only 6 links in 1 minute. Try later]'
        elif shorter == 'is.gd':
            response = requests.get(f'https://is.gd/create.php?format=simple&url={urllib.parse.quote(url)}')
            out = response.text
        elif shorter == 'vk.cc':
            response = requests.get(f'https://api.vk.com/method/utils.getShortLink?url={urllib.parse.quote(url)}&access_token={vkcc_api_key}&v=5.131')
            answer = json.loads(response.text)
            out = (answer['response']['short_url'])
        else:
            out = url

        return out

    except:
        return f'[Unexpected error. Contact with developer]'

# Generate link for posting in external groups
def make_utm_ext(url, ext_groups):
    campaign = url.split('/')[-1]
    for item in ext_groups:

        out = f'{item}: '

        url_utm = f'{url}?utm_source=facebook&utm_medium=social&utm_campaign={campaign}&utm_term={item}'
        out += short_link(url_utm, 'cutt.ly')

        print (out)

# Generate link for posting in external groups
def make_utm_our(url, terms):
    campaign = url.split('/')[-1]
    for item in terms:
        source = item['utm_source']
        term = item['utm_term']
        shorter = item['shorter']

        out = f'{source}: '

        url_utm = f'{url}?utm_source={source}&utm_medium=social&utm_campaign={campaign}&utm_term={term}'
        out += short_link(url_utm, shorter)

        print (out)


url = 'https://link/to/blog/post'

# < ========================================= >
# If you want use one of these functions,
# just comment another
# < ========================================= >

# Post into group1
make_utm_our(url, terms_group1)

# Post into group2
make_utm_our(url, terms_group2)

# Post in external groups
ext_groups = [
    'external_group1_name',
    'external_group2_name'
]
make_utm_ext(url, ext_groups)