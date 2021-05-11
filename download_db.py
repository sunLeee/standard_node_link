import os
import datetime
import wget
import zipfile
import logging

from selenium import webdriver

def open_driver(headless=True, url = "https://www.its.go.kr/nodelink/nodelinkRef") :
    options = webdriver.ChromeOptions()
    if headless :
        options.headless = True
    else :
        pass
    options.add_argument('window-size=1920x2160')
    options.add_argument("disable-gpu")
#     options.add_argument('Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/88.0.4324.150 Safari/537.36')
    options.add_argument("lang=ko_KR") # 한국어!
    base_url = url
    driver = webdriver.Chrome(chrome_options=options)
    driver.get(base_url)
    return driver    

def make_directory(name='db') :
    if name not in os.listdir() :
        os.makedirs("./"+name)
    else :
        pass

def find_latest_name_url(driver) :
    download_name = str(driver.find_element_by_partial_link_text("NODELINKDATA.zip").text).split(".zip")[0]
    download_url = driver.find_element_by_partial_link_text("NODELINKDATA.zip").get_attribute("href")
    return download_name, download_url
    
def make_screenshot(driver) :
    make_directory("screenshot")
    driver.get_screenshot_as_file('./screenshot/screenshot_'+datetime.datetime.now().strftime("%Y-%m-%d-%H%M%S")+'.jpg')
    
def download_latest_file(download_name, download_url) :
    compressed_name = "./db/"+download_name+'.zip'
    print(f"\n{download_name}의 다운로드를 시작합니다.")
    wget.download(download_url, compressed_name )
    print("\n다운로드를 완료하였습니다.")
    zipfile.ZipFile(compressed_name).extractall("./db/"+download_name)
    print("\n압축해제를 완료하였습니다.")
    
def main() :
    # output.csv가 있으면 읽어서 compareness_before를 읽어드림
    # output.csv가 없으면 만들고 헤더부분 넣는다
    try : 
        with open('./output.csv', 'r') as f :
            lines = f.readlines()
            compareness_before = lines[-1].split(",")[1]
    except FileNotFoundError : 
        with open('./output.csv', 'w') as f :
            f.write('checked_date,latest_version,url')
            compareness_before = None
        print("there is no output file so I made it")

    # Chrome Drive Open
    driver = open_driver(True)
    # Directory 만들기
    [make_directory(name) for name in ['db','screenshot']]
    # ScreenShot 남기기
    make_screenshot(driver)
    # name, url 확인
    latest_name, latest_url = find_latest_name_url(driver)
    # output에 글을쓰고, 
    with open('./output.csv', 'a') as f:
        today = datetime.datetime.now().strftime("%Y-%m-%d")
        f.write('\n')
        f.write(today)
        f.write(',')
        f.write(latest_name[:12])
        f.write(',')
        f.write(latest_url)

    # 최신것이 아니면, db 디렉토리에 다운로드 및 압축 해제
    if compareness_before != latest_name[:12] :
        download_latest_file(download_name=latest_name, download_url=latest_url)
        
if __name__ == "__main__" :
    main()