from news_connector import load_news_and_market


def main():
	news, market = load_news_and_market(max_articles=3)
	print("news count", len(news))
	print("market count", len(market))
	print("market", market)


if __name__ == "__main__":
	main()
