import os
import wget
import zipfile
from selenium import webdriver

def open_driver(headless=True, url = "https://www.its.go.kr/nodelink/nodelinkRef") :
    options = webdriver.ChromeOptions()
    if headless :
        options.headless = True
    else :
        pass
    options.add_argument('window-size=1920x2160')
    options.add_argument("lang=ko_KR") # 한국어!
    driver = webdriver.Chrome(chrome_options=options)
    driver.get(url)
    return driver

def make_directory(name='db') :
    if name not in os.listdir() :
        os.makedirs("./"+name)
    else :
        pass
           
def main() :
    # Chrome Drive Open
    driver = open_driver(True)
    # Directory 만들기
    make_directory("map_db")
    # name, url 확인
    download_name = str(driver.find_element_by_partial_link_text("NODELINKDATA.zip").text).split(".zip")[0]
    download_url = driver.find_element_by_partial_link_text("NODELINKDATA.zip").get_attribute("href")
    
    print(f"\n{download_name}의 다운로드를 시작합니다.")
    compressed_name = "./map_db/"+download_name+'.zip'
    wget.download(download_url, compressed_name )
    print("\n다운로드를 완료하였습니다.")
    zipfile.ZipFile(compressed_name).extractall("./map_db/"+download_name)
    print("\n압축해제를 완료하였습니다.")

if __name__ == "__main__" :
    main()