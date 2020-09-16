
from src.Scrapper import Scrapper
from src.Scrapper import Cleaner


def start():
    data = Scrapper().get_data()
    Cleaner(data).clean()


if __name__ == '__main__':
    start()
