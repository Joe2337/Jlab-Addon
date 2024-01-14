import webbrowser
import urllib.parse

class WebSearch:

    @staticmethod
    def googleTranslate(input):
        urlPrefix = u"https://translate.google.com/#view=home&op=translate&sl=ja&tl=en&text="
        url = urlPrefix + urllib.parse.quote(input)
        WebSearch.openUrl(url)

    @staticmethod
    def googleForGrammar(input):
        base = u"https://google.com/search?q=japanese grammar "
        url =  base + urllib.parse.quote(input)
        WebSearch.openUrl(url)

    @staticmethod
    def jgram(input):
        urlPrefix = u"http://www.jgram.org/pages/viewList.php?s="
        urlSuffix = u"&search.x=0&search.y=0"
        url =  urlPrefix + input + urlSuffix
        WebSearch.openUrl(url)

    @staticmethod
    def verbixConjugate(input):
        urlPrefix = u"https://www.verbix.com/webverbix/Japanese/"
        urlSuffix = u""
        url =  urlPrefix + urllib.parse.quote(input) + urlSuffix
        WebSearch.openUrl(url)

    @staticmethod
    def verbixDeinflect(input):
        urlPrefix = u"https://www.verbix.com/find-verb/"
        urlSuffix = u""
        url =  urlPrefix + urllib.parse.quote(input) + urlSuffix
        WebSearch.openUrl(url)

    @staticmethod
    def openUrl(url):
        webbrowser.open(url)
        #webbrowser.open_new_tab(url) # the webbrowser module is not included in anki
        #QDesktopServices.openUrl(QUrl.fromEncoded(bytearray(url, "utf-8")))

