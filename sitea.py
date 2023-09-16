import requests
from bs4 import BeautifulSoup
from interface_class import *
from helper_class import *
from proxy_interface import *
from database_interface import *
import json
import time


class quebecmedecin:
    def __init__(self):
        self.lastpage = 0
        self.helper = Helper()
        self.all_data = []

    def get_category(self):
        url = "https://www.quebecmedecin.com/medecin/rechercher-un-medecin.htm"
        response = requests.get(url)
        soup = BeautifulSoup(response.content, 'lxml')
        specialties = soup.find('select', {'id': 'DoctorSpecialties'})
        
        if specialties:
            option_elements = specialties.find_all('option')
            self.Specialties = [option.get('value') for option in option_elements if option.get('value') is not None and option.get('value') != '']
            
            # print(self.Specialties)
        else:
            print("Specialties dropdown not found on the page.")
        return self.Specialties
    

    def get_doctor_response(self,id):
        url=f'https://www.quebecmedecin.com/medecin/rechercher-un-medecin.htm/page:2?data%5BDoctor%5D%5Bspecialties%5D={id}&data%5BDoctor%5D%5Bcity_id%5D=&data%5BDoctor%5D%5Bnom%5D=&data%5BDoctor%5D%5Bprenom%5D=&data%5BDoctor%5D%5Bcodepostal%5D='
        # print(i)
        response_last=requests.get(url) 
        #time.sleep(5)
        soup=BeautifulSoup(response_last.content,"html.parser")
        page=soup.find("h1",{'class':'h4'})
        if page:
            self.lastpage=page.text.split('/')[-1]
        else:
            self.lastpage=1
        print("ids:",id,"pages:",self.lastpage)
        for p in range(1,int(self.lastpage)+1):
            response = requests.get(
                f'https://www.quebecmedecin.com/medecin/rechercher-un-medecin.htm/page:{p}?data%5BDoctor%5D%5Bspecialties%5D={id}&data%5BDoctor%5D%5Bcity_id%5D=&data%5BDoctor%5D%5Bnom%5D=&data%5BDoctor%5D%5Bprenom%5D=&data%5BDoctor%5D%5Bcodepostal%5D=')
            self.Doctors_links(response,id)
        
    def Doctors_links(self,response,i):
        soup = BeautifulSoup(response.content, 'lxml')
        divs = soup.find_all("div", {'class': 'strip_list wow fadeIn'})
        listing = []

        for detail in divs:
            url = "https://www.quebecmedecin.com" + self.helper.get_url_from_tag(detail.find("a", {'class': 'text-dark'}))
            listing.append(url)

        self.filtered_urls = [url for url in listing if url != "https://www.quebecmedecin.com"]

        for link in self.filtered_urls:
            self.Scrap_data(link)

    def Scrap_data(self, link):
        data =[]
        obj = {
            'Doctor_name': '',
            'category': '',
            'Address': '',
            'phone_number': '',
            'Specialites': [],
            'permis': '',
            'Statut': '',
            'Assurance': '',
            'Recommandations': []
        }
        response = requests.get(link)
        soup = BeautifulSoup(response.content, 'lxml')
        divs = soup.find('div', {'class': 'col-lg-8 col-md-9'})
        
        obj['Doctor_name'] = self.helper.get_text_from_tag(divs.find('h1'))
        obj['category'] = self.helper.get_text_from_tag(divs.find('small'))
        
        ul_tag = divs.find("ul", {'class': 'contacts'})
        obj['Address'] = self.helper.get_text_from_tag(ul_tag.find('li')).replace("Adresse principale", "Main Adress").replace("Voir sur la carte", "").strip()
        obj['Address'] = re.sub(r'\s+', ' ', obj['Address']).strip()
        
        obj['phone_number'] = self.helper.get_text_from_tag(ul_tag.find('a', {'rel': 'nofollow'}))
        
        Specialites_tag = soup.find('ul', {'class': 'bullets'})
        Specialite = Specialites_tag.find_all('li')
        obj['Specialites'] = [self.helper.get_text_from_tag(spe) for spe in Specialite]
        
        div_class = soup.find_all('div', {'class': 'col-lg-12'})[-1]
        if div_class:
            permis_items = div_class.find_all('li')
            if len(permis_items) >= 3:
                obj['permis'] = permis_items[0].get_text()
                obj['Statut'] = permis_items[1].get_text()
                obj['Assurance'] = permis_items[2].get_text()
            else:
                print("Not enough <li> elements found within the last 'col-lg-12' div.")
        else:
            print("No 'col-lg-12' div found on the page.")
        
        Recommandations_tag = soup.find_all('div', {'class': 'review-box clearfix'})
        obj['Recommandations'] = [self.helper.clean_text(re.sub(r'\s+', ' ', Recomma.get_text()), ensure_ascii=False) for Recomma in Recommandations_tag]

        print(json.dumps(obj, ensure_ascii=False))
        self.all_data.append(obj)

    def scrapy(self):
        ids = self.get_category()
        print(ids)
        self.run_multiThread(
            self.get_doctor_response,
            3,
            ids
        )
        print("datas lenth:-------------------",len(self.all_data))
        with open("AllDoctorsData.json", "w", encoding="utf-8") as json_file:
            json.dump(self.all_data, json_file, ensure_ascii=False, indent=4)
        
    def run_multiThread(self, function, max_workers, args):
        with concurrent.futures.ThreadPoolExecutor(max_workers=max_workers) as executor:
            executor.map(function, args)

if __name__ == "__main__":
    obj = quebecmedecin()
    obj.scrapy()
    # obj.Scrap_data('https://www.quebecmedecin.com/medecin/medecin-chaput-miguel-3872.htm')