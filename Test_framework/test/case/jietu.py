# from selenium import webdriver                  #从selenium库导入webdirver
from selenium.webdriver.chrome.options import Options
# import time
chrome_options = Options()
chrome_options.add_argument("--disable-extensions")
          

from selenium import webdriver
import time

def take_screenshot(url, save_fn="capture.png"):
    #browser = webdriver.Firefox() # Get local session of firefox
    #browser = webdriver.Chrome(chrome_options=chrome_options)
    browser = webdriver.PhantomJS(executable_path=r'.\phantomjs-2.1.1-windows\bin\phantomjs.exe',service_args=['--ignore-ssl-errors=true', '--ssl-protocol=TLSv1']) 
    browser.set_window_size(1500, 900)
    browser.get(url) # Load page

    browser.execute_script("""
        (function () {
            var y = 0;
            var step = 100;
            window.scroll(0, 0);

            function f() {
                if (y < document.body.scrollHeight) {
                    y += step;
                    window.scroll(0, y);
                    setTimeout(f, 100);
                } else {
                    window.scroll(0, 0);
                    document.title += "scroll-done";
                }
            }

            setTimeout(f, 1000);
        })();
    """)

    for i in range(30):
        if "scroll-done" in browser.title:
            break
        time.sleep(10)

    browser.save_screenshot(save_fn)
    browser.close()
def date_time(delta):
    now = datetime.date.today()
    delta2 = datetime.timedelta(days=1)
    delta = datetime.timedelta(days=delta)
    n_days = now-delta2 - delta
    return (n_days.strftime('%Y-%m-%d'))

if __name__ == "__main__":
    import xlrd
    import datetime,os
    comment =  xlrd.open_workbook(r'test.xls')#(),encoding='utf-8',errors='ignore'
    table = comment.sheets()[0] 
    nrows = table.nrows
    ncols = table.ncols
    product = table.row_values(0)[1]
    filepath = '.\\'+product+'\\'+date_time(-1)+'\\'
    if not os.path.exists(filepath):
        os.makedirs(filepath)
    for i in range(1,nrows):

        
        name = '.\\'+product+'\\'+date_time(-1)+'\\'+str(i)+table.row_values(i)[1]+'.png'
        url = table.row_values(i)[2]
        print (name)
        take_screenshot(url,name)
