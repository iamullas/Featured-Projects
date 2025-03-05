import requests
from bs4 import BeautifulSoup


def scrape_books(url, output_csv):
    response = requests.get(url)
    soup = BeautifulSoup(response.text, 'html.parser')
    books = soup.find_all('article', class_='product_pod')

    with open(output_csv, 'w') as file:
        file.write("Title,Price,Rating\n")
        for book in books:
            title = book.h3.a['title']
            price = book.find('p', class_='price_color').text
            rating = book.p['class'][1]
            file.write(f"{title},{price},{rating}\n")
    print(f"Data saved to {output_csv}!")


# Example usage (test with books.toscrape.com):
scrape_books('http://books.toscrape.com', 'books_data.csv')