from selenium import webdriver
from selenium.webdriver.chrome.options import Options
import schedule
import time
import tweepy

def download_image():
    options = Options()
    options.add_argument("--headless")

    driver = webdriver.Chrome(options=options)
    driver.get("http://explosm.net/rcg")
    time.sleep(5) # allow a few seconds for comic to load

    # find the comic and scroll to it
    comicElement = driver.find_element_by_xpath('//*[@id="rcg-speed-strip"]')
    driver.execute_script("arguments[0].scrollIntoView();", comicElement)

    # screenshot the comic and save it
    with open('comic.png', 'wb') as file:
        file.write(comicElement.screenshot_as_png)

    driver.quit()


def post_to_twitter():
    download_image()

    #twitter app keys and tokens
    api_key ="xxxxxxxxxxxxxxxxxxxxx"
    api_secret ="xxxxxxxxxxxxxxxxxxxxx"
    access_token ="xxxxxxxxxxxxxxxxxxxxx"
    access_token_secret ="xxxxxxxxxxxxxxxxxxxxx"
    
    # authentication 
    auth = tweepy.OAuthHandler(api_key, api_secret) 
    auth.set_access_token(access_token, access_token_secret)
    api = tweepy.API(auth)

    try:
        api.verify_credentials()
    except:
        print("Error during authentication")
    
    # post to twitter
    api.update_with_media('./comic.png')


if __name__ == '__main__':
    schedule.every(10).minutes.do(post_to_twitter)
    
    while True:
        schedule.run_pending()
        time.sleep(1)
