import urllib
from bs4 import BeautifulSoup

html = urllib.urlopen('https://news.ycombinator.com/').read()

soup = BeautifulSoup(html, "html.parser")
[s.extract() for s in soup(['style', 'script'])]

text = soup.getText()
lines = (line.strip() for line in text.splitlines())
chunks = (phrase.strip() for line in lines for phrase in line.split("  "))
text = '\n'.join(chunk for chunk in chunks if chunk)

print text