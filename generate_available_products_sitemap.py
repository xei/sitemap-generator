import sys
import mysql.connector
from mysql.connector import Error


DB_HOST = 'localhost'
DB_NAME = sys.argv[1]
DB_USER_NAME = sys.argv[2]
DB_PASS = sys.argv[3]

FILE_NAME = 'daily-available-products-sitemap.xml'

PRODUCT_DETAILS_URL = 'https://www.example.com/{lang}/products/{id}'
LANGS = ['fa', 'en']

FIND_AVAILABLE_PRODUCTS_QUERY = "SELECT id, lastmod FROM product WHERE status = 'AVAILABLE'"


urls_count = 0


def write_urls_to_file(file, product):
  id = product['id']
  lastmod = product['lastmod'].strftime('%F')

  alternate_tags = ''
  for lang in LANGS:
    alternate_tags += "\n\t\t<xhtml:link\n\t\t\trel=\"alternate\"\n\t\t\threflang=\"{lang}\"\n\t\t\thref=\"{href}\"/>".format(lang = lang, href = PRODUCT_DETAILS_URL.format(lang = lang, id = id))

  file.write("\n\t<url>\n\t\t<loc>{location}</loc>\n\t\t<lastmod>{lastmod}</lastmod>{alternate_tags}\n\t</url>".format(location = PRODUCT_DETAILS_URL.format(lang = 'fa', id = id), lastmod = lastmod, alternate_tags = alternate_tags))

  global urls_count
  urls_count += 1


with open(FILE_NAME, "w") as file:
  print("File %s opened." % FILE_NAME)

  file.write('<?xml version="1.0" encoding="UTF-8"?>\n<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9"\n\txmlns:xhtml="http://www.w3.org/1999/xhtml">')

  try:
    cnx = mysql.connector.connect(host=DB_HOST,
				database=DB_NAME,
				user=DB_USER_NAME,
				password=DB_PASS)
    print("Connection to database established.")

    cursor = cnx.cursor(dictionary=True)

    print("Please wait a moment...")

    cursor.execute(FIND_AVAILABLE_PRODUCTS_QUERY)
    available_products = cursor.fetchall()
    
    for product in available_products:
      write_urls_to_file(file, product)

    print('%d URLs are added.' % urls_count)
    if urls_count > 50000:
      print('WARNING: each sitemap file must have at last 50000 links!')

  except Error as e:
    print("Unfortunately there is an error!", e)
  finally:
    if cnx.is_connected():
      cursor.close()
      cnx.close()
      print("Connection to database closed.")

  file.write('\n</urlset>')

print('Sitemap is ready!')
