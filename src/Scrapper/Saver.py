
class Saver:

    def __init__(self, data):
        self.df = data

    def save(self):
        self.df.to_csv("quotes.csv")
