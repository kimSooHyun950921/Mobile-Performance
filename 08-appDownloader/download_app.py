import csv
import time
import pandas as pd
import selenium
from selenium import webdriver
from selenium.webdriver.common.keys import Keys

def read_applist(filename):
    with open(filename) as csvfile:
        reader = csv.DictReader(csvfile)
        for row in reader:
            change_list = []
            split_str = row['category'].split('_')
            for word in split_str:
                if word == "GAME":
                    change_list.append(word)
                    break
                if word == 'AND':
                    change_list.append('&')
                else:
                    new_word = word[0]+word[1:].lower()
                    change_list.append(new_word)
            category = ' '.join(change_list)
            yield category, row['package_name'], row['appname']


def main(FLAGS):
    driver = webdriver.Chrome('./Driver/chromedriver')
    app_list = []
    if FLAGS.name == "package":
        for category, package, appname in read_applist(FLAGS.filename):
            app_list.append({"Category":category,"AppName":appname, "PackageName":package})
            print(category,package,appname)
            driver.get(f'https://play.google.com/store/apps/details?id={package}')
            links = driver.find_elements_by_tag_name("button")
            if len(links) == 0 :
                continue
            for link in links:
                if link.text == "Install" or link.text == "Installed":
                    break
            #if link.text == "Installed":
            #    print("installed")
            #    continue
            link.click()
            time.sleep(5)
            try:
                sign_in = driver.find_elements_by_tag_name("button")
                for sign in sign_in:
                    if sign.text == "Sign in":
                        break
                sign.click()
                time.sleep(4)
                driver.find_element_by_xpath('/html/body/div[1]/div[1]/div[2]/div/div[2]/div/div/div[2]/div/div[1]/div/form/span/section/div/div/div[1]/div/div[1]/div/div[1]/input').send_keys("testshkim12@gmail.com")
                driver.find_element_by_xpath('/html/body/div[1]/div[1]/div[2]/div/div[2]/div/div/div[2]/div/div[2]/div/div[1]/div/div/button').click()
                time.sleep(2)
                driver.find_element_by_name("password").send_keys("tngus6357")
                driver.find_element_by_xpath('/html/body/div[1]/div[1]/div[2]/div/div[2]/div/div/div[2]/div/div[2]/div/div[1]/div/div/button').click()
            except Exception as e:
                print(e)
            time.sleep(20)
            disabled=True
            iframes = driver.find_elements_by_tag_name("iframe")
            for iframe in iframes:
                driver.switch_to.frame(iframe)
                try:

                    button = driver.find_element_by_xpath("/html/body/div/div/div[2]/div[3]/span/button")
                    disabled = driver.execute_script("return arguments[0].hasAttribute(\"disabled\");", button)
                    if disabled == False:
                        button.click()
                    else:
                        break
                except Exception as e:
                    driver.switch_to_default_content()
            if disabled == True:
                continue
            time.sleep(4)
            
            driver.find_element_by_name("password").send_keys("tngus6357")
            driver.find_element_by_xpath('/html/body/div[1]/div[1]/div[2]/div/div[2]/div/div/div[2]/div/div[2]/div/div[1]/div/div/button').send_keys(Keys.RETURN)
            time.sleep(20)

            iframes = driver.find_elements_by_tag_name("iframe")
            for iframe in iframes:
                driver.switch_to.frame(iframe)
                try:
                    button = driver.find_element_by_xpath("/html/body/div/div/div[2]/div[3]/button").click()
                    break
                except Exception as e:
                    driver.switch_to_default_content()

            time.sleep(4)
            df = pd.DataFrame(app_list)
            df.to_csv('test-app.csv', index=False)


if __name__=="__main__":
    import argparse
    parser = argparse.ArgumentParser(description='download app list')
    parser.add_argument('--filename', '-f',
                        required=True,
                        type=str,
                        help='input applist csv')
    parser.add_argument('--name', '-n', 
                         default='package',
                         help='package or appname')
    FLAGS = parser.parse_args()
    main(FLAGS)
