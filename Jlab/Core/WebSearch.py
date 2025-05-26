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
    def verbixConjugate(input):
        urlPrefix = "https://www.verbix.com/webverbix/Japanese/"
        urlSuffix = ""
        url = urlPrefix + urllib.parse.quote(input) + urlSuffix
        WebSearch.openUrl(url)

    @staticmethod
    def japaneseVerbConjugator(input):
        urlPrefix = "https://www.japaneseverbconjugator.com/VerbDetails.asp?txtVerb="
        urlSuffix = "&Go=Conjugate"
        url = urlPrefix + urllib.parse.quote(input) + urlSuffix
        WebSearch.openUrl(url)

    @staticmethod
    def jishoLookup(input):
        urlPrefix = "https://jisho.org/search/"
        urlSuffix = ""
        url = urlPrefix + urllib.parse.quote(input) + urlSuffix
        WebSearch.openUrl(url)

    @staticmethod
    def openUrl(url):
        webbrowser.open(url)
        # webbrowser.open_new_tab(url) # the webbrowser module is not included in anki
        # QDesktopServices.openUrl(QUrl.fromEncoded(bytearray(url, "utf-8")))
