import webbrowser
import urllib.parse


class WebSearch:

    @staticmethod
    def googleTranslate(input):
        urlPrefix = "https://translate.google.com/#view=home&op=translate&sl=ja&tl=en&text="
        url = urlPrefix + urllib.parse.quote(input)
        WebSearch.openUrl(url)

    @staticmethod
    def googleForGrammar(input):
        base = "https://google.com/search?q=japanese grammar "
        url = base + urllib.parse.quote(input)
        WebSearch.openUrl(url)

    @staticmethod
    def jgram(input):
        urlPrefix = "http://www.jgram.org/pages/viewList.php?s="
        urlSuffix = "&search.x=0&search.y=0"
        url = urlPrefix + input + urlSuffix
        WebSearch.openUrl(url)

    @staticmethod
    def verbixConjugate(input):
        urlPrefix = "https://www.verbix.com/webverbix/Japanese/"
        urlSuffix = ""
        url = urlPrefix + urllib.parse.quote(input) + urlSuffix
        WebSearch.openUrl(url)

    @staticmethod
    def verbixDeinflect(input):
        urlPrefix = "https://www.verbix.com/find-verb/"
        urlSuffix = ""
        url = urlPrefix + urllib.parse.quote(input) + urlSuffix
        WebSearch.openUrl(url)

    @staticmethod
    def openUrl(url):
        webbrowser.open(url)
        # webbrowser.open_new_tab(url) # the webbrowser module is not included in anki
        # QDesktopServices.openUrl(QUrl.fromEncoded(bytearray(url, "utf-8")))
