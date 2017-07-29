from imagetypersapi import ImageTypersAPI
try:
    from selenium import webdriver
except:
    raise Exception('selenium package missing. Install with: pip install selenium')
try:
    import requests as req
except:
    raise Exception('requests package missing. Install with: pip install requests')
try:
    from lxml import html
except:
    raise Exception('lxml package missing. Install with: pip install lxml')

from time import sleep

# ----------------------------------------------------------
# credentials
IMAGETYPERS_USERNAME = 'testingfor'
IMAGETYPERS_PASSWORD = 'testingfor'

# recaptcha test page
TEST_PAGE_NORMAL = 'http://192.168.1.19:8000/recaptcha_normal.php'
TEST_PAGE_INVISIBLE = 'http://192.168.1.19:8000/recaptcha_invisible.php'
# ----------------------------------------------------------

# browser (selenium) test
def browser_test_normal():
    print '[=] BROWSER TEST STARTED (NORMAL RECAPTCHA) [=]'
    d = webdriver.Chrome()      # open browser
    try:
        d.get(TEST_PAGE_NORMAL)               # go to test page
        # complete regular info
        d.find_element_by_name('first_name').send_keys('Kevin')
        d.find_element_by_name('last_name').send_keys('O\'ryan')
        d.find_element_by_name('email').send_keys('kevin@oryanzzw.com')

        print '[+] Completed regular info'

        # get sitekey from page
        site_key = d.find_element_by_class_name('g-recaptcha').get_attribute('data-sitekey')
        print '[+] Site key: {}'.format(site_key)

        #print '[+] Waiting for recaptcha to be solved ...'
        # complete captcha
        #i = ImageTypersAPI(IMAGETYPERS_USERNAME, IMAGETYPERS_PASSWORD)
        #recaptcha_id = i.submit_recaptcha(TEST_PAGE_NORMAL, site_key)      # submit recaptcha
        #while i.in_progress(recaptcha_id):      # check if still in progress
        #    sleep(10)       # every 10 seconds

        #g_response_code = i.retrieve_recaptcha(recaptcha_id)        # get g-response-code
        g_response_code = raw_input('CODE:')

        print '[+] Got g-response-code: {}'.format(g_response_code) # we got it
        javascript_code = 'document.getElementById("g-recaptcha-response").innerHTML = "{}";'.format(g_response_code)
        d.execute_script(javascript_code)       # set g-response-code in page (invisible to the 'naked' eye)
        print '[+] Code set in page'

        # submit form
        d.find_element_by_tag_name('form').submit()     # submit form
        print '[+] Form submitted'
        print '[+] Page source: {}'.format(d.page_source)     # show source
        sleep(10)
    finally:
        d.quit()        # quit browser
        print '[=] BROWSER TEST FINISHED [=]'

# requests test
def requests_test_normal():
    print '[=] REQUESTS TEST STARTED (NORMAL RECAPTCHA) [=]'
    try:
        print '[+] Getting sitekey from test page...'
        resp = req.get(TEST_PAGE_NORMAL)      # make request and get response
        tree = html.fromstring(resp.text)                               # init tree for parsing
        site_key = tree.xpath('//div[@class="g-recaptcha"]')[0].attrib['data-sitekey']  # get sitekey
        print '[+] Site key: {}'.format(site_key)

        # solve captcha
        print '[+] Waiting for recaptcha to be solved ...'
        # complete captcha
        i = ImageTypersAPI(IMAGETYPERS_USERNAME, IMAGETYPERS_PASSWORD)
        recaptcha_id = i.submit_recaptcha(TEST_PAGE_NORMAL, site_key)  # submit recaptcha
        while i.in_progress(recaptcha_id):  # check if still in progress
            sleep(10)  # every 10 seconds

        #g_response_code = raw_input('CODE:')
        g_response_code = i.retrieve_recaptcha(recaptcha_id)  # get g-response-code
        print '[+] Got g-response-code: {}'.format(g_response_code)  # we got it

        # make request with data
        resp = req.post(TEST_PAGE_NORMAL, data={
            'first_name' : 'Kevin',
            'last_name' : 'O\'ryan',
            'email' : 'kevin@oryanzzw.com',
            'g-recaptcha-response' : g_response_code
            }
        )
        print '[+] Form submitted'
        print '[+] Response: {}'.format(resp.text.encode('utf-8'))

    finally:
        print '[=] REQUESTS TEST FINISHED [=]'

# browser (selenium) test - invisible
def browser_test_invisible():
    print '[=] BROWSER TEST STARTED (INVISIBLE RECAPTCHA) [=]'
    d = webdriver.Chrome()      # open browser
    try:
        d.get(TEST_PAGE_INVISIBLE)               # go to test page
        # complete regular info
        d.find_element_by_name('first_name').send_keys('Kevin')
        d.find_element_by_name('last_name').send_keys('O\'ryan')
        d.find_element_by_name('email').send_keys('kevin@oryanzzw.com')

        print '[+] Completed regular info'

        # get sitekey from page
        site_key = d.find_element_by_class_name('g-recaptcha').get_attribute('data-sitekey')
        data_callback = d.find_element_by_class_name('g-recaptcha').get_attribute('data-callback')
        print '[+] Site key: {}'.format(site_key)
        print '[+] Callback method: {}'.format(data_callback)

        print '[+] Waiting for recaptcha to be solved ...'
        # complete captcha
        i = ImageTypersAPI(IMAGETYPERS_USERNAME, IMAGETYPERS_PASSWORD)
        recaptcha_id = i.submit_recaptcha(TEST_PAGE_INVISIBLE, site_key)      # submit recaptcha
        while i.in_progress(recaptcha_id):      # check if still in progress
            sleep(10)       # every 10 seconds

        #g_response_code = raw_input('CODE:')
        g_response_code = i.retrieve_recaptcha(recaptcha_id)        # get g-response-code

        print '[+] Got g-response-code: {}'.format(g_response_code) # we got it
        javascript_code = 'document.getElementById("g-recaptcha-response").innerHTML = "{}";'.format(g_response_code)
        d.execute_script(javascript_code)       # set g-response-code in page (invisible to the 'naked' eye)
        print '[+] Code set in page'

        # submit form
        d.execute_script('{}();'.format(data_callback))
        print '[+] Form submitted (through JavaScript)'
        print '[+] Page source: {}'.format(d.page_source)     # show source
        sleep(10)
    finally:
        d.quit()        # quit browser
        print '[=] BROWSER TEST FINISHED [=]'

# requests test - invisible
def requests_test_invisible():
    print '[=] REQUESTS TEST STARTED (INVISIBLE RECAPTCHA) [=]'
    try:
        print '[+] Getting sitekey from test page...'
        resp = req.get(TEST_PAGE_INVISIBLE)      # make request and get response
        tree = html.fromstring(resp.text)                               # init tree for parsing
        site_key = tree.xpath('//button[@class="g-recaptcha"]')[0].attrib['data-sitekey']  # get sitekey
        print '[+] Site key: {}'.format(site_key)

        # solve captcha
        print '[+] Waiting for recaptcha to be solved ...'
        # complete captcha
        i = ImageTypersAPI(IMAGETYPERS_USERNAME, IMAGETYPERS_PASSWORD)
        recaptcha_id = i.submit_recaptcha(TEST_PAGE_INVISIBLE, site_key)  # submit recaptcha
        while i.in_progress(recaptcha_id):  # check if still in progress
            sleep(10)  # every 10 seconds

        #g_response_code = raw_input('CODE:')
        g_response_code = i.retrieve_recaptcha(recaptcha_id)  # get g-response-code
        print '[+] Got g-response-code: {}'.format(g_response_code)  # we got it

        # make request with data
        resp = req.post(TEST_PAGE_INVISIBLE, data={
            'first_name' : 'Kevin',
            'last_name' : 'O\'ryan',
            'email' : 'kevin@oryanzzw.com',
            'g-recaptcha-response' : g_response_code
            }
        )
        print '[+] Form submitted'
        print '[+] Response: {}'.format(resp.text.encode('utf-8'))

    finally:
        print '[=] REQUESTS TEST FINISHED [=]'

def main():
    print '[==] TESTS STARTED [==]'
    print '--------------------------------------------------------------------'
    try:
        browser_test_normal()
        print '--------------------------------------------------------------------'
        requests_test_normal()
        print '--------------------------------------------------------------------'
        browser_test_invisible()
        print '--------------------------------------------------------------------'
        requests_test_invisible()
    except Exception, ex:
        print '[!] Error occured: {}'.format(ex)
        print '[==] ERROR [==]'
    finally:
        print '--------------------------------------------------------------------'
        print '[==] TESTS FINISHED [==]'

if __name__ == "__main__":
    main()