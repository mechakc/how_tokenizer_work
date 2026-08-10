import urllib.request

url = "https://www.gutenberg.org/cache/epub/4650/pg4650.txt"
urllib.request.urlretrieve(url, "candide.txt")

with open("candide.txt", encoding="utf-8") as f:
    text = f.read()

print(len(text), "caractères")