from selenium import webdriver
from selenium.common import NoSuchElementException
from selenium.webdriver.common.by import By
import csv

#открытие файла для записи
w_file = open("data.csv","w")
names = ["ID","Title","Link","Actual Price","Old Price","Company"]
file_writer = csv.DictWriter(w_file, delimiter=";",
                             lineterminator="\r", fieldnames=names)
file_writer.writeheader()

#подключение
link = 'https://online.metro-cc.ru/'
driver = webdriver.Edge()
driver.get(link)
driver.implicitly_wait(10)

button_online = driver.find_element(By.CSS_SELECTOR,".simple-button.reset-button.catalog--online.offline-prices-sorting--best-level.item__input.item__input--online")
button_online.click()


button_online = driver.find_element(By.CSS_SELECTOR,"button.rectangle-button.reset--button-styles.action-button.apply-button.blue.lg.normal.wide")
button_online.click()

water_btn = driver.find_element(By.LINK_TEXT,"Вода")
water_btn.click()

pages = driver.find_elements(By.CSS_SELECTOR,"ul.catalog-paginate a")
links = [element.get_attribute("href") for element in pages]

#цикл по страницам
for link in links:
    driver.get(link)
    driver.implicitly_wait(5)
    table_products = driver.find_element(By.ID,'products-inner')
    products = table_products.find_elements(By.CSS_SELECTOR,'.catalog-2-level-product-card')

    #цикл по плиткам с водой
    for product in products:
        # Доступ к информации о товаре
        id = product.get_attribute('data-sku')
        title = product.find_element(By.CSS_SELECTOR,'.product-card-photo__link').get_attribute('title')
        link = product.find_element(By.CLASS_NAME,'product-card-photo__link').get_attribute("href")
        prices_element = product.find_element(By.CLASS_NAME,'product-card-prices__content-prices')

        actual_price_element = prices_element.find_element(By.CLASS_NAME,'product-card-prices__actual')
        actual_price_rub = actual_price_element.find_element(By.CLASS_NAME,'product-price__sum-rubles').text
        try:
            actual_price_penny = actual_price_element.find_element(By.CLASS_NAME,'product-price__sum-penny').text
        except:
            actual_price_penny = 0
        actual_price = float(actual_price_penny)+float(actual_price_rub)

        try:
            old_price_element = prices_element.find_element(By.CLASS_NAME,'product-card-prices__old')
            old_price_rub = old_price_element.find_element(By.CLASS_NAME,'product-price__sum-rubles').text
            try:
                old_price_penny = old_price_element.find_element(By.CLASS_NAME,'product-price__sum-penny').text
            except:
                old_price_penny = 0
            old_price = float(old_price_rub)+float(old_price_penny)

        except NoSuchElementException:
            old_price = actual_price



        # Вывод информации о товаре
        row = {'ID': id,
        'Title': title,
        'Link': link,
        "Actual Price": actual_price,
        "Old Price": old_price,
        "Company": title.split(",")[0]}
        file_writer.writerow(row)

print("информация записана")
