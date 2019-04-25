import pywikibot
site = pywikibot.Site('en', 'wikipedia')  # any site will work, this is just an example
page = pywikibot.Page(site, 'President')
item = pywikibot.ItemPage.fromPage(page)  # this can be used for any page object
# you can also define an item like this

dictionary = item.get()  # you need to call it to access any data.
print(dictionary.keys())

