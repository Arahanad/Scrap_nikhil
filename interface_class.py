# -*- coding: utf-8 -*-
from helper_class import *
from proxy_interface import *
from selenium.webdriver.common.desired_capabilities import DesiredCapabilities

class INTERFACING():

    def __init__(self):

        self.helper = Helper()
        self.driver_initialized = False
        self.driver = ''
        self.MAX_TRIALS = 2

        self.use_proxy = True

        if self.use_proxy:
            self.proxy_filename = 'data.json'
            self.pluginfile = 'proxy_auth_plugin.zip'
        
        self.driver_path = './../web_driver/chromedriver'

        self.proxy_handle = CWEBSHARE()

    def process_browser_logs_for_network_events(self):

        logs = self.driver.get_log("performance")

        for entry in logs:

            try:
                log = json.loads(entry["message"])["message"]['params']['headers']
                _log = log['authorization']
                _log = log['x-correlation-id']
                _log = log['cookie']

                return log

            except:
                continue

        return {}
            

    def proxy_json_data(self):

        if not self.helper.is_file_exist(self.proxy_filename):
            self.proxy_handle.get_proxy_list(self.proxy_filename)

        proxy_date = self.helper.read_json_file(self.proxy_filename)['date']
        current_date = self.helper.get_time_stamp().split()[0]
        
        if proxy_date != current_date:
            self.proxy_handle.get_proxy_list(self.proxy_filename)

        all_proxies = self.helper.read_json_file(self.proxy_filename)['proxies']

        while 1:
            random_index = random.randint(0,len(all_proxies)-1)
            current_proxy = all_proxies[random_index]
            if current_proxy['valid']:
                break

        # ylyncxyw  :  zweu7p3c0xln  :  154.92.112.235  :  5256
        PROXY_USER = current_proxy['username']
        PROXY_PASS = current_proxy['password']
        PROXY_HOST = current_proxy['proxy_address']
        PROXY_PORT = current_proxy['ports']['socks5']

        print(PROXY_USER," : ",PROXY_PASS," : ",PROXY_HOST," : ",PROXY_PORT)

        manifest_json = """
        {
            "version": "1.0.0",
            "manifest_version": 2,
            "name": "Chrome Proxy",
            "permissions": [
            "proxy",
            "tabs",
            "unlimitedStorage",
            "storage",
            "<all_urls>",
            "webRequest",
            "webRequestBlocking"
            ],
            "background": {
            "scripts": ["background.js"]
            },
            "minimum_chrome_version":"22.0.0"
        }
        """

        background_js = """
            var config = {
                mode: "fixed_servers",
                rules: {
                    singleProxy: {
                        scheme: "http",
                        host: "%s",
                        port: parseInt(%s)
                    },
                    bypassList: ["localhost"]
                }
            };

            chrome.proxy.settings.set({value: config, scope: "regular"}, function() {});

                    function callbackFn(details) {
                    return {
                    authCredentials: {
                    username: "%s",
                    password: "%s"
                }
            };
        }

        chrome.webRequest.onAuthRequired.addListener(
        callbackFn,
        {urls: ["<all_urls>"]},
        ['blocking']
        );
        """ % (PROXY_HOST, PROXY_PORT, PROXY_USER, PROXY_PASS)

        with zipfile.ZipFile(self.pluginfile, 'w') as zp:
            zp.writestr("manifest.json", manifest_json)
            zp.writestr("background.js", background_js)

    def get_url_response(self,url):   

        count = 0
        while count < self.MAX_TRIALS:
            try:
                print("Processing URL: " , url,)
                agent = {
                        "User-Agent":'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/85.0.4183.121 Safari/537.36'
                        }
                        
                html = requests.get(url,headers=agent).text
                return html
            except Exception as error:
                print('Error in getting URL Response: ',error)

            count += 1

    def make_soup(self):
        return BeautifulSoup(self.driver.page_source, 'lxml')

    def make_soup_url(self,page_url):
        return BeautifulSoup(self.get_url_response(page_url), 'lxml')

    def current_url(self):
        return self.driver.current_url

    def get_driver(self):

        
        opts = Options()
        opts.add_argument("user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/99.0.4844.51 Safari/537.36")
        
        if self.use_proxy:
            self.proxy_json_data()
            opts.add_extension(self.pluginfile)
        
        if 0:
            self.driver = webdriver.Chrome(self.driver_path, options=opts)
        else:
            capabilities = DesiredCapabilities.CHROME
            capabilities["goog:loggingPrefs"] = {"performance": "ALL"}  # chromedriver 75+
            self.driver = webdriver.Chrome("./chromedriver", options=opts, desired_capabilities=capabilities)

        self.driver_initialized = True

    def add_cookie(self,cookie):
        self.driver.add_cookie(cookie)
        
    def close_driver(self):

        if self.driver_initialized:
            self.driver.quit()
            print("Closed the driver")
            self.driver_initialized = False

    def get_selenium_response(self,url):
        try:
            if not self.driver_initialized:
                self.get_driver()
            else:
                pass

            self.driver.get(url)
            sleep_time = 3
            time.sleep(sleep_time)
            
        except Exception as error:
            print('Error in getting Selenium response: ',error)

        return self.make_soup()

    def get_page_source(self):
        return self.driver.page_source

    def clicking(self,xpath):
        elem = self.driver.find_element_by_xpath(xpath)
        elem.click()
        time.sleep(random.randint(2,3))

    def entering_values(self,xpath,value):
        elem = self.driver.find_element_by_xpath(xpath)
        elem.clear()
        elem.send_keys(value)
        time.sleep(random.randint(1,2))

    def going_back(self):
        self.driver.execute_script("window.history.go(-1)")
        time.sleep(1)

    def scroll_continuous_down(self):
        SCROLL_PAUSE_TIME = 3

        # Get scroll height
        last_height = self.driver.execute_script("return document.body.scrollHeight")

        while True:
            # Scroll down to bottom
            print("Scrolling Down....")
            self.driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")

            # Wait to load page
            time.sleep(SCROLL_PAUSE_TIME)

            # Calculate new scroll height and compare with last scroll height
            new_height = self.driver.execute_script("return document.body.scrollHeight")
            if new_height == last_height:
                break
            last_height = new_height

if __name__ == "__main__":
    handle = INTERFACING()
    handle.proxy_json_data()
    handle.get_driver()
