import re
import selenium
import pandas as pd
from selenium import webdriver
import time
import random
def read_category_list():
    category_list = pd.read_csv('applist/category_list.csv')['category_list'].to_list()
    return category_list


def main():
    saved_index = 1
    saved_cat_index = 0
    cat_list = read_category_list()
    p = re.compile('android-most-popular-google-play-apps\?category=.*')
    dict_list = []
    while len(cat_list) > 0:
        try:
            driver = webdriver.Chrome('./Driver/chromedriver')
            saved_index = 1
            category = cat_list.pop(0)
            while saved_index < 40:
                driver.get(f'https://www.androidrank.org/android-most-popular-google-play-apps?start={saved_index}&sort=4&price=all&category={category}')
                table = driver.find_element_by_id('ranklist')
                elements = table.find_elements_by_tag_name('a')
                for element in elements:
                    url = element.get_attribute('href')
                    package_name = url.split('/')[-1]
                    appname = element.text
                    if p.match(package_name) == None:
                        print(package_name, appname)
                        dict_list.append({"PackageName":package_name, "AppName":appname})
                time.sleep(random.randint(6,12))
                saved_index += 20
            df = pd.DataFrame(dict_list)
            df.to_csv(f"data/top40/{category}.csv", index=False)
            dict_list = []
        except Exception as e:
            print(e)
            driver.close()
            cat_list.insert(0, category)


if __name__ == "__main__":
    main()
