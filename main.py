from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import csv

driver = webdriver.Chrome()
driver.implicitly_wait(7)

link_page = 'https://eme54.ru/'
list_articles = []


# Writing articles from file to list
with open('list_articles.csv', 'r', encoding='utf-8-sig') as f:
    reader = csv.reader(f, delimiter = ';')
    for row in reader:
        list_articles.append(' '.join(row))


def link_crawling():
    link_crawling_list = []

    for article in list_articles:
        try:
            link_crawling_list_row = []

            search_field = WebDriverWait(driver, 10).until(EC.visibility_of_element_located((By.CSS_SELECTOR, '.bx-form-control'))) # search field on start and other page
            search_field.click()
            search_field.send_keys(article)

            WebDriverWait(driver, 10).until(EC.invisibility_of_element_located((By.ID, 'smart-title-search_preloader_item'))) # Waiting to loading search animation is stopped

            WebDriverWait(driver, 5).until(EC.visibility_of_element_located((By.CSS_SELECTOR, '.bx_item_block_item_name_flex_align'))).click() # Click on the first element on search result
            
            link_crawling_list_row.append(article) # append article to list
            link_crawling_list_row.append(WebDriverWait(driver, 10).until(EC.visibility_of_element_located((By.CSS_SELECTOR, 'h1'))).text) # append name of good to list
            link_crawling_list_row.append(driver.current_url) # append url to list
            link_crawling_list.append(link_crawling_list_row) # append temporarty list-row to big list of lists

        except Exception as ex:
                link_crawling_list.append(link_crawling_list_row)
                print(ex)
                driver.get(url=link_page)
                continue
        
    with open('result_list.csv', 'w') as f:
        writer = csv.writer(f, delimiter=';', lineterminator='\n')
        for item in link_crawling_list:
            writer.writerow(item)
    return



try:
    driver.get(url=link_page)
    driver.maximize_window()
    if __name__ == '__main__':
        link_crawling()
        print('Done')

except Exception as ex:
    print(ex)
    pass

finally:
    driver.close()
    driver.quit()

