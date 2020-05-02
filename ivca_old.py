from selenium import webdriver
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from selenium.common.exceptions import TimeoutException
from selenium.common.exceptions import NoSuchElementException
import csv
import requests
from bs4 import BeautifulSoup
from selenium.webdriver.common.keys import Keys


class VetFinder():
    def __init__(self):
        self.driver = webdriver.Chrome(executable_path="/home/pratik/Documents/chromedriver")

        self.driver.get("https://ivca.de/veterinary-chiropractor-search/")
        self.result = []
        with open('zipcode_usa.csv') as f:
             self.records = [{k: v for k, v in row.items()}
        for row in csv.DictReader(f, skipinitialspace=True)]


    def get_link(self, href):
        d = webdriver.Chrome(executable_path="/home/pratik/Documents/chromedriver")
        d.get(href)
        #with open("source.html", "w") as fp:
            #fp.write(d.page_source)
        return d.page_source

    #all = driver.find_element_by_css_selector("div[id='sidebar']")
    def save_to_csv(self, result):
        keys = result[0].keys()
        with open('ivca_old.csv', 'w') as output_file:
            dict_writer = csv.DictWriter(output_file, keys)
            dict_writer.writeheader()
            dict_writer.writerows(result)

    def scrape(self):
        for record in self.records:
            zipcode = record["ZIP"].strip()
            search = self.driver.find_element_by_css_selector("input[name='snear']")
            #print(len(search))
            #Search = search.find_element_by_css_selector("input")
            #Search.click()
            print(zipcode)
            search.send_keys(zipcode)
            

            Search = self.driver.find_elements_by_class_name("geodir_submit_search")[0]
            Search.click()

            delay = 10 # seconds
            try:
                myElem = WebDriverWait(self.driver, delay).until(EC.presence_of_element_located((By.ID, 'IdOfMyElement')))
                print ("Page is ready!")
            except TimeoutException:
                print ("Loading took too much time!")
            try:
                Con = self.driver.find_element_by_css_selector("div[class='geodir-loop-container']")
                all_con = Con.find_elements_by_css_selector("li")
                #print(all_con.text)


                for con in all_con:
                                #Item = con.find_elements_by_css_selector("h2[class='geodir-entry-title'")
                                #print(len(item))
                    Href = con.find_element_by_css_selector("a")
                    href = Href.get_attribute("href")
                                #print(href)
                                #new(href)

                    source = self.get_link(href)
                    soup = BeautifulSoup(source,"lxml")


                    Category = ""
                    try:
                        category = soup.find("div", {"class":"geodir-field-post_category"})
                        c = category.find("a")
                        Category = c.getText()
                    except:
                            pass
                                    #print(Cat)

                    Name = ""
                    Title = ""
                    First_Name = ""
                    Last_Name = ""
                    Others_certiifications = ""
                    try:
                        name = soup.find("article")
                        n = name.find("h1",{"class":'entry-title main_title'})
                        Name = n.getText()
                        Title = Name.split(" ")[0]
                        First_Name = Name.split(" ")[1]
                        Last_Name = Name.split(" ")[2]
                        certificate = Name.split(" ")[3:] 
                        certificate.append(Title)
                        #print(First_Name)
                        #print(Last_Name)
                        #print(Others_certiifications)
                    except:
                            pass

                    Address = ""
                    try:
                        address = soup.find("div", {"class":"geodir-field-address"})
                        a1 = address.find("span", {"itemprop":"streetAddress"})
                        A1 = a1.getText()
                        a2 = address.find("span", {"itemprop":"addressLocality"})
                        A2 = a2.getText()
                        a3 = address.find("span", {"itemprop":"addressRegion"})
                        A3 = a3.getText()
                        a4 = address.find("span", {"itemprop":"postalCode"})
                        A4 = a4.getText()
                        a5 = address.find("span", {"itemprop":"addressCountry"})
                        A5 = a5.getText()
                        Address = A1 +", "+ A2 +", "+A3 +", "+ A4 + ", "+A5


                                    #print(Address)
                    except:
                            pass
                                #print(Add)

                    Phone = ""
                    try:
                        phone = soup.find("div", {"class":"geodir-field-phone"})
                        p = phone.find("a")
                        Phone = p.getText()
                    except:
                        pass
                                #print(Phn)
                    Email = ""
                    try:
                        email = soup.find("div", {"class":"geodir-field-email"})              
                        e = email.find("a")
                        Email = e.getText()
                    except:
                            pass
                                #print(Email)

                    Website = ""
                    try:
                        website = soup.find("div", {"class":"geodir-field-website"})              
                        w = website.find("a")
                                    #print(w)
                        Website = w.get("href")
                                    #print(Website)
                    except:
                        pass


                    Facebook = ""
                    try:
                        facebook = soup.find("div", {"class":"geodir-field-facebook"})              
                        f = facebook.find("a")
                                    #print(f)
                        Facebook = f.get("href")
                                    #print(Facebook)
                    except:
                        pass
                                
                    tmp = {
                        "Clinic_Name":"",
                        "First_Name":First_Name,
                        "Last_Name":Last_Name,
                        "Address":A1,
                        "City":A2,
                        "State" :A3,
                        "Zip":A4,
                        "Country":A5,                
                        "Phone":Phone,
                        "Email":Email,
                        "Website":Website,
                        #"Facebook":Facebook,
                        #"Category":Category,
                        #"Title":Title 
                        "Certificate":certificate
                           }
                    print(tmp)
                    self.result.append(tmp)
                    self.save_to_csv(self.result)
            except:
                continue
            self.driver.execute_script("window.history.go(-1)")
        return self.result
vf = VetFinder()

#print(zipcode)
result = vf.scrape()
print(result)



