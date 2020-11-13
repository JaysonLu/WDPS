from bs4 import BeautifulSoup

class Html2TextConveter:

	def __init__(self, payload):
		self.payload = payload

	def text(self):
		soup = BeautifulSoup(self.payload.raw_stream.read(), "lxml")
		for script in soup(["script", "style", "head"]):
			script.extract()    # rip it out
		html_text = soup.get_text()

		lines = (line.strip() for line in html_text.splitlines())
		chunks = (phrase.strip() for line in lines for phrase in line.split("  "))
		text = '\n'.join(chunk for chunk in chunks if chunk)
		return text


