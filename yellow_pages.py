### get number,email,name,websites
from requests_html import HTML
from selenium import webdriver
import csv
import os

class Yellowpage_sscrape:

    def __init__(self,business,location,pages):
        self.business = business
        self.location = location
        self.pages = pages+1
        self.list = []
        
        # this makes selenium run in the back
        self.options = webdriver.ChromeOptions()
        self.options.add_argument("headless")
        #######################################
        
        self.driver = webdriver.Chrome(executable_path=r'C:\Program Files (x86)\chromedriver.exe', options=self.options)
        print('active')
        self.get_links()
        print(len(self.list))

    def get_links(self):
        for page in range(1,self.pages):
            url = f"https://www.yellowpages.com/search?search_terms={self.business}&geo_location_terms={self.location}&page={page}"
            self.driver.get(url)
            src = self.driver.page_source
            r = HTML(html=src)
            links = r.find('a.business-name')
            for link in links:
                print('https://www.yellowpages.com' + link.attrs['href'])
                self.list.append('https://www.yellowpages.com' + link.attrs['href'])


    def get_link_info(self):
        #this gets individual links page source document
        for link in self.list:
            self.driver.get(link)
            src = self.driver.page_source
            r = HTML(html= src)
            self.get_deets(r)


    def get_deets(self,r):
        b_ness = {}
        
        titles = r.find('h1',first=True)
        print(titles.text)
        b_ness['Name'] = titles.text
        
        
        try:
            e_mail = r.find('a.email-business',first = True)
            print('Email: '+e_mail.attrs['href'].replace('mailto:', ''))
        except:
            b_ness['Email'] = 'none'
        else:
            b_ness['Email'] = e_mail.attrs['href'].replace('mailto:', '')
    
        try:
          
            phone = r.find('p.phone',first = True)
            print("Number: "+phone.text)
            
        except:
          
            b_ness['Number'] = 'none'
            
        else:
          
            b_ness['Number'] = phone.text
            
            
        try:
          
          
            h2_tag = r.find('div.contact', first=True)
            h = h2_tag.find('h2.address')
            a = h[-1]
            print(a.text)
            
        except:
          
            b_ness.setdefault('Address', 'none')
            
        else:
          
            b_ness.setdefault('Address',a.text)  
            
        try:

            website = r.find('a.primary-btn.website-link',first = True)
            print( "Web links:"+ website.attrs['href'])
            
        except:
          
            b_ness.setdefault('Website', 'none')
            print('nil')
            
        else:

            b_ness.setdefault('Website',website.attrs['href'])
        print(b_ness)
        self.write_csv(b_ness)

    def write_csv(self,b_ness):
        
        if not os.path.exists('business'):
            os.mkdir('business')
        file = 'business/business.csv'
        values = [b_ness['Website'],b_ness['Address'],b_ness['Number'],b_ness['Email'],b_ness['Name']]
        with open(file, 'a') as f:
            writer = csv.writer(f)
            writer.writerow(values)

if __name__ == '__main__':
    lists = Yellowpage_sscrape(business='pizza',location = 'Broomfield, CO',pages = 2)
    lists.get_link_info()
    lists.driver.quit()
