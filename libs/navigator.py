import time
import re
import json
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options

types = {
    "xpath": By.XPATH,
    "tag":   By.TAG_NAME,
    "id":    By.ID,
    "name":  By.NAME,
    "class": By.CLASS_NAME,
    "css"  : By.CSS_SELECTOR
}

class Element :

    element=None 

    def __init__(self, element) -> None:
        self.element = element

    def getValueOf(self, att:str) -> str:
        return self.element.get_attribute(att)

    def getText(self) -> str:
        try:
            text = self.element.get_attribute('innerText')
            return text
        except:
            print("Erro no Element não foi possível pegar o InnerText da publicação")
            return ""
    
    def value(self, text=""):
        self.element.send_keys(text)
    
    def click(self) :
        try:
            self.element.click()
            return True
        except:
            return False


class Navigator :

    driver   = None 
    file     = None
    site     = ""
    scrollm  = 1

    def __init__(self, site, headless=False) -> None:
        
        options = Options()
        options.add_experimental_option('prefs', {'intl.accept_languages': 'pt,pt_BR', "profile.default_content_setting_values.notifications" : 2})
        if headless:
            options.add_argument('--headless=new')
        self.driver = webdriver.Chrome(executable_path='chromedriver', chrome_options=options)
        self.driver.set_window_size(2560, 1440)
        self.site = site
        self.setUrl()
        self.driver.get(self.site)
        if self.getState():
            self.driver.get(self.site)
    
    def exec(self, script:str) -> str | bool:
        try:
            return self.driver.execute_script(script)
        except:
            return False

    def scrooldown(self, body=True):
        if not body:
            to = 1500 * self.scrollm
            self.driver.execute_script(f"""
                let height = "{to}";
                window.scrollTo(0, height);
            """)
            self.scrollm += 1
        else:
            self.driver.execute_script(f"window.scrollTo(0, document.body.scrollHeight);")

    def goto(self, url, full=False):
        self.saveState()
        self.driver.get(url if full else self.site+url)

    def currentUrl(self):
        return self.driver.current_url

    def setUrl(self) :
        if self.file is None:
            pattern = '(https:\/\/)?(www\.)?(\w+\.\w+)'
            matches = re.finditer(pattern, self.site)
            for match in matches:
                self.file = match.group(3)

    def getState(self) :
        try :
            file    = open('./cookies/'+self.file+'.json','r')
            cookies = json.loads(file.read())
            for cookie in cookies:
                self.driver.add_cookie(cookie)
            file.close()
            return True
        except :
            return False

    def saveState(self) :
        cookies = self.driver.get_cookies()
        file    = open('./cookies/'+self.file+'.json','w')
        file.write(json.dumps(cookies))
        file.close()

    def findElements(self, type, value, limit=15, element:Element=None) -> list[Element] | bool:
        naoEncontrou=True
        count=0
        els=[]
        finder = element.element if element != None else self.driver
        while naoEncontrou and count < limit:
            try:
                if   type == 'text':
                    elements = finder.find_elements(types['xpath'], "//*[text()='"+value+"']")  
                elif type == 'link':
                    elements = finder.find_elements(types['xpath'], "//a[text()='"+value+"']")
                elif type == 'placeholder':
                    elements = finder.find_elements(types['xpath'], "//input[@placeholder='"+value+"']")
                elif type == 'button':
                    elements = finder.find_elements(types['xpath'], "//button[text()='"+value+"']")
                else: 
                    elements = finder.find_elements(types[type], value)
                naoEncontrou= False
            except:
                time.sleep(1)
                count = count + 1
        for element in elements:
            els.append(Element(element=element))
        return False if naoEncontrou else els
    

    def findElement(self, type, value, limit=15, element:Element=None) -> Element | bool:
        naoEncontrou=True
        count=0
        el=None
        finder = element.element if element != None else self.driver
        while naoEncontrou and count < limit:
            try:
                if   type == 'text':
                    element = finder.find_element(types['xpath'], "//*[text()='"+value+"']")  
                elif type == 'link':
                    element = finder.find_element(types['xpath'], "//a[text()='"+value+"']")
                elif type == 'placeholder':
                    element = finder.find_element(types['xpath'], "//input[@placeholder='"+value+"']")
                elif type == 'button':
                    element = finder.find_element(types['xpath'], "//button[text()='"+value+"']")
                else: 
                    #print("tentando -> "+value)
                    element = finder.find_element(types[type], value)
                el = Element(element)
                naoEncontrou= False
            except:
                time.sleep(1)
                count = count + 1

        return False if naoEncontrou else el

    def press(self):
        # preciona tecla do teclado
        return self
    
    def sleep(self, sec=0):
        sec = sec * -1 if sec < 0 else sec
        # print(sec)
        if sec == 0:
            while True:
                time.sleep(1)
        else:
            time.sleep(sec)
    