from services.publish_service import getPublishByMedia, updatePub
from spiders.youtube.youtube_lib import extract_time_to_minutes
from libs.navigator import Navigator
import re 
from datetime import datetime, timedelta

async def repair_data():

    navigator = Navigator("https://youtube.com", headless=True)

    publishList = await getPublishByMedia('youtube')
    for pub in publishList:
        
        navigator.goto(pub.getLink(), full=True)
        navigator.sleep(1)
        
        el = navigator.findElement("xpath", "//ytd-watch-info-text//span[3]", 15)
        now = datetime.now()

        if not el: continue
        
        match = re.match(r'.+(\d+)\s*(dias?|semanas?|meses?|anos?)', el.getText())
        
        if not match: continue

        quantidade = int(match.group(1))
        periodo = match.group(2).lower()
        
        if 'dia' in periodo:
            delta = timedelta(days=quantidade)
        elif 'semana' in periodo:
            delta = timedelta(weeks=quantidade)
        elif 'mes' in periodo:
            delta = timedelta(days=30 * quantidade)
        elif 'ano' in periodo:
            delta = timedelta(days=365 * quantidade)
        else:
            continue
        result_date = now - delta
        datafinal = result_date.strftime('%Y-%m-%d 00:00:00')
        pub.setData(datafinal)


    for pub in publishList:
        print(pub.getData())
        print(pub.getLink())
        print(pub.getId())
        stats = await updatePub(pub)
        print(stats)

    print("reparação finalizada")
    navigator.sleep()

    


