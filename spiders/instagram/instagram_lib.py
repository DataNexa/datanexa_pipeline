
from entidades.Publish import Publish
from libs.navigator import Navigator
from datetime import date,timedelta
import re

# sem, min, d, h
# fazer o calculo de quantidade de dias atrás e salvar
# testar o midia config verificando se é adicionado a publicação com as config

def generatePublish(text:str, link:str) -> Publish: 
    

    tex = text.split("Ver tradução")[0]
    dat = re.search("(\d+)\s(sem|min|d|h)([^\w]|$)", tex)
    
    infnum = int(dat.group(1))
    inftyp = dat.group(2)

    hoje = date.today()

    if inftyp == 'sem': infnum *= 7
    
    data = f"{hoje}" if inftyp in ['min', 'h'] else f"{hoje - timedelta(days=infnum)}"

    pub = Publish(midiaSlug="instagram", titulo="Publicação Instagram", text=tex, link=link)
    pub.setData(data)

    return pub



def login(navigator:Navigator) -> None:

    inputEmail= navigator.findElement("name", "username", 5)
    
    if inputEmail != False:
        try:

            c = navigator.getAccount()

            inputEmail.click()
            inputEmail.value(c["email"])

            inputSenha = navigator.findElement("name", "password", 1)

            inputSenha.click()
            inputSenha.value(c["senha"]) 

            navigator.findElement("text", "Entrar", 3).click()
            navigator.sleep(10)
            navigator.saveState()

        except:
            pass

def checkPop(navigator:Navigator):
    pop = navigator.findElement("button", "Agora não", limit=3)
    if pop != False: pop.click() 


def pesquisa(navigator:Navigator, hashTag:str) -> bool:

    tag = hashTag.replace("#", "")
    navigator.goto(f"explore/tags/{tag}/")
    
    primeiraPub = navigator.findElement("xpath", '//article//a[1]', 5)
    
    if primeiraPub != False: 
        primeiraPub.click()
        return True

    return False


def getPublish(navigator:Navigator) -> Publish:
    
    try :
        els = navigator.findElements("tag", "article", 10)
        pub = generatePublish(els[1].getText(), navigator.currentUrl())
        return pub
    except:
        return None


def next(navigator:Navigator) -> bool:
    try :
        tests = [
            '/html/body/div[6]/div[1]/div/div[3]/div/div/div/div/div[1]/div/div/div[2]/button',
            '/html/body/div[7]/div[1]/div/div[3]/div/div/div/div/div[1]/div/div/div/button',
            '/html/body/div[6]/div[1]/div/div[3]/div/div/div/div/div[1]/div/div/div/button'
        ]
        i = 0
        btns = False
        while i < len(tests):
            btns = navigator.findElement("xpath", tests[i], limit=3)
            if btns: break
            i += 1

        if btns == False: 
            return False
        btns.click()
        return True
    except:
        print("erro ao tentar apertar NEXT")
        return False
    
    
    
