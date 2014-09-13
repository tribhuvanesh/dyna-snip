import requests
import json
import base64

import urllib2
import lxml
from lxml import etree
from lxml.html import parse, submit_form

GITHUB_CODE_SEARCH_URL_PAT = "https://github.com/search?l=%s&q=%s&ref=searchresults&type=Code"
GITHUB_CODE_SEARCH_COUNT_XPATH_PAT = "//*[@id='code_search_results']/div[1]"
GITHUB_CODE_SEARCH_RES_XPATH_PAT = "//*[@id='code_search_results']/div[1]/div[%d]/p/a[1]"
GITHUB_CODE_SEARCH_PATH_XPATH_PAT = "//*[@id='code_search_results']/div[1]/div[%d]/p/a[2]"


def get_snippet_list(query, lang):
    # Scrape Github's code search page for this query
    # Assume query is some sort of string, ex. "create twilio rest client"
    response = urllib2.urlopen(GITHUB_CODE_SEARCH_URL_PAT % (lang, '+'.join(query.split())) + "&utf8=%E2%9C%93")
    html = response.read()
    pg   = lxml.html.fromstring(html)

    # Check how many results have been returned
    res_count = len(pg.xpath(GITHUB_CODE_SEARCH_COUNT_XPATH_PAT)[0].getchildren())

    # If #results > 0, just return the snippet from the first result
    if res_count > 0:
        # Obtain the repo name, owner name and then call Github code search API
        uname_repo_ele = pg.xpath(GITHUB_CODE_SEARCH_PATH_XPATH_PAT % (1))[0]
        # ele.atrib['href'] returns something like '/user/repo1'
        uname, repo = uname_repo_ele.attrib['href'].split('/')[1:3]
        file_path = uname_repo_ele.attrib['title']
        print uname, repo, file_path

        # Now use the github code search api in this repo to obtain the file
        hint_content = requests.get('https://api.github.com/repos/%s/%s/contents/%s' % (uname, repo, file_path))
        sug = json.loads(hint_content.text)
        print base64.decodestring(sug['content'])


def main():
    get_snippet_list("create twilio rest client", "java")


if __name__ == '__main__':
    main()

