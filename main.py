import time
import datetime
import praw
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
SUB_REDDITS = ["IdiotsInCars", "failarmy", "Iamactuallyverybadass", "maybemaybemaybe", "WhyWereTheyFilming", "blackmagicfuckery", "ViralSnaps", "yesyesyesyesno", "nonononoyes", "nevertellmetheodds", "Whatcouldgowrong", "WTF", "WatchPeopleDieInside", "SweatyPalms", "PublicFreakout", "nextfuckinglevel", "KidsAreFuckingStupid", "interestingasfuck", "HumansBeingBros", "holdmyredbull", "funny", "FuckingWithNature", "Damnthatsinteresting", "ContagiousLaughter", "aww", "LivestreamFail"]

reddit = praw.Reddit(client_id='',
                     client_secret='',
                     user_agent='',
                     username='',
                     password='')

posts = open("data/posts.txt", encoding='utf-8').read().splitlines()  # list of all previously posted titles
postsToday = []                                                       # list of today's post data
today = datetime.datetime.today()
chrome_options = Options()

postsPerSub = 12

def getposts():
    global postsFromSub
    sessionposts = []
    postsFromSub = 0
    for sub in SUB_REDDITS:                                           # go through each subreddit
        for post in reddit.subreddit(sub).hot(limit=postsPerSub*10):   # get top posts
            if postsFromSub < postsPerSub and post.url not in posts:  # check if duplicate post and if its needed
                posts.append(post.url)
                sessionposts.append(post.url)
                try:
                    if not post.is_self and not post.media['reddit_video']['is_gif']:
                        postsToday.append(post)
                        print(sub + ": " + str(postsFromSub + 1) + "/" + str(postsPerSub))
                        postsFromSub += 1
                except:
                    pass
            elif postsFromSub >= postsPerSub:
                postsFromSub = 0
                break
    postsToday.sort(key=lambda pst: pst.score, reverse=True)
    with open('data/posts.txt', 'a', encoding='utf-8') as postdata:
        for line in sessionposts:
            postdata.write(line + '\n')
    downloadposts()

    time.sleep(86400)  # wait a day for next post collection


def downloadposts(progress=0, downloaded=0):
    chrome_options.add_experimental_option("prefs", {
        "download.default_directory": r"D:\Programming\Pycharm Projects\TopToInsta\videos\{0}".format(
            str(today.date())),
        "download.prompt_for_download": False,
        "download.directory_upgrade": True,
        "safebrowsing.enabled": True
    })

    for post in postsToday:
        try:
            progress += 1
            driver = webdriver.Chrome("venv/chromedriver.exe", options=chrome_options)
            driver.get("https://ripsave.com/")
            time.sleep(1)

            input_field = driver.find_element_by_name("url")
            input_field.send_keys(post.url)

            input_button = driver.find_element_by_css_selector("button#_button")
            input_button.click()

            time.sleep(3)
            if driver.find_elements_by_tag_name("i")[1].get_attribute('innerHTML') == "Video with Audio ♪":
                downloads = driver.find_elements_by_css_selector("table.downloadTable td a")
                downloads[0].click()
                downloaded += 1
                time.sleep(7)
            driver.close()
            print("Progress: " + str(progress) + "/" + str(len(postsToday)) + ", Downloaded: " + str(downloaded))
        except:
            print("Progress: " + str(progress) + "/" + str(len(postsToday)) + ", Downloaded: " + str(downloaded))
            pass
    print("\n----- C O M P L E T E -----")


getposts()
