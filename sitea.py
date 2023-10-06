import requests
from bs4 import BeautifulSoup
from interface_class import *
from helper_class import *
from proxy_interface import *
from database_interface import *
import json
import pandas as pd



class quebecmedecin:
    def __init__(self):
        self.lastpage = 0
        self.helper = Helper()
        self.all_data = []
        self.Recommandation = []

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
        url=f'https://www.quebecmedecin.com/medecin/rechercher-un-medecin.htm/page:2?data%5BDoctor%5D%5Bspecialties%5D=&data%5BDoctor%5D%5Bcity_id%5D=&data%5BDoctor%5D%5Bnom%5D={id}&data%5BDoctor%5D%5Bprenom%5D=&data%5BDoctor%5D%5Bcodepostal%5D='
        # print(i)
        response_last=requests.get(url) 
        #time.sleep(5)
        soup=BeautifulSoup(response_last.content,"html.parser")
        page=soup.find("h1",{'class':'h4'})
        if page:
            lastpage=page.text.split('/')[-1]
        else:
            lastpage=1

        print("================================>","ids:",id,"pages:",lastpage)

        ps = [i for i in range(1,int(lastpage)+1)]
        ids = [id for i in range(1,int(lastpage)+1)]
        # for p in range(1,int(lastpage)+1):
        
        with concurrent.futures.ThreadPoolExecutor(max_workers=20) as executor:
            executor.map(self.Doctors_links, ps,
            ids)
        
    def Doctors_links(self,p,id):
        print(len(self.all_data),p,'start')
        response = requests.get(
            f'https://www.quebecmedecin.com/medecin/rechercher-un-medecin.htm/page:{p}?data%5BDoctor%5D%5Bspecialties%5D=&data%5BDoctor%5D%5Bcity_id%5D=&data%5BDoctor%5D%5Bnom%5D={id}&data%5BDoctor%5D%5Bprenom%5D=&data%5BDoctor%5D%5Bcodepostal%5D=')
        # self.Doctors_links(response,id)
        soup = BeautifulSoup(response.content, 'lxml')
        divs = soup.find_all("div", {'class': 'strip_list wow fadeIn'})
        listing = []

        for detail in divs:
            url = "https://www.quebecmedecin.com" + self.helper.get_url_from_tag(detail.find("a", {'class': 'text-dark'}))
            listing.append(url)

        filtered_urls = [url for url in listing if url != "https://www.quebecmedecin.com"]

        iis = [ id for k in filtered_urls]

        with concurrent.futures.ThreadPoolExecutor(max_workers=20) as executor:
            executor.map(self.Scrap_data, filtered_urls,
            iis)
        
        # for link in filtered_urls:
        #     self.Scrap_data(link,i)

    def Scrap_data(self, link,i):
        obj = {
            'link':'',
            'Doctor_name': '',
            'category': '',
            'Address': '',
            'phone_number': '',
            'Specialites': [],
            'permis': '',
            'Status': '',
            'Assurance': '',
            'Recommandation' :[],
            'Active':'',
            'Status_discription':''
        }
        response = requests.get(link)
        soup = BeautifulSoup(response.content, 'lxml')
        divs = soup.find('div', {'class': 'col-lg-8 col-md-9'})
        if 'Inactive' in soup.text:
            obj['Active'] = False
        else:
            obj['Active'] = True

        obj['link'] = link
        print(link)
        obj['Doctor_name'] = self.helper.get_text_from_tag(divs.find('h1'))
        obj['category'] = self.helper.get_text_from_tag(divs.find('small'))
        
        ul_tag = divs.find("ul", {'class': 'contacts'})
        try:
            obj['Address'] = self.helper.get_text_from_tag(ul_tag.find('li')).replace("Adresse principale", "Main Adress").replace("Voir sur la carte", "").replace('Main Adress','').strip()
            obj['Address'] = re.sub(r'\s+', ' ', obj['Address']).strip()
        except:
            obj['Address'] = ''
        try:

            obj['phone_number'] = self.helper.get_text_from_tag(ul_tag.find('a', {'rel': 'nofollow'}))
        except:
            obj['phone_number'] = ''
        Specialites_tag = soup.find('ul', {'class': 'bullets'})
        Specialite = Specialites_tag.find_all('li')
        obj['Specialites'] = [self.helper.get_text_from_tag(spe) for spe in Specialite]
        
        div_class = soup.find_all('div', {'class': 'col-lg-12'})[-1]
        if div_class:
            permis_items = div_class.find_all('li')

            for item in permis_items:
                if 'permis' in item.get_text():
                    obj['permis'] = permis_items[0].get_text().replace("Numéro de permis : ","")
                if 'Statut' in item.get_text():
                    obj['Statut'] = permis_items[1].get_text().replace("Statut :","")
                if 'Assurance' in item.get_text():
                    obj['Assurance'] = permis_items[2].get_text().replace("Assurance :","")

        else:
            print("No 'col-lg-12' div found on the page.")
        Recommandations_tag = soup.find_all('div', {'class': 'review-box clearfix'})
        Recommandations = [self.helper.clean_text(re.sub(r'\s+', ' ', Recomma.get_text()), ensure_ascii=False) for Recomma in Recommandations_tag]
        for recommendation in Recommandations:
            # Use regular expressions to extract name, date, and text
            match = re.match(r"(.+) – (\d{2} \w+ \d{4}) : (.+)", recommendation)
            if match:
                name = match.group(1)
                date = match.group(2)
                description = match.group(3)
                self.Recommandation.append({
            "name": name,
            "Date": date,
            "Description": description
        })
                obj['Recommandation'].append({
            "name": name,
            "Date": date,
            "Description": description
        })
        Statut_description = soup.find('div',{'class':'alert alert-danger'})
        if Statut_description:
            obj['Statut_discription'] = self.helper.get_text_from_tag(Statut_description)
        else:
            obj['Statut_discription'] = ""
        # print(json.dumps(obj, ensure_ascii=False))
        self.all_data.append(obj)
        print(len(self.all_data),i,'done')
        # data.append(obj)
        # csv_file_path = "output.csv"
        # fieldnames = ["Doctor_name", "category", "Address", "phone_number", "Specialites", "permis", "Statut", "Assurance", "Name", "Date", "Recommandation"]
        # with open(csv_file_path, mode='w', newline='', encoding='utf-8') as csv_file:
        #     writer = csv.DictWriter(csv_file, fieldnames=fieldnames)
        #     writer.writerows(data)

    def scrapy(self):
        # ids = self.get_category()
        ids = ['A', 'B', 'C', 'D', 'E', 'F', 'G', 'H', 'I', 'J', 'K', 'L', 'M', 'N', 'O', 'P', 'Q', 'R', 'S', 'T', 'U', 'V', 'W', 'X', 'Y', 'Z']
        # ids = ['A']
        print(ids)
        # for i in ids:
        #     self.get_doctor_response(i)
        self.run_multiThread(
            self.get_doctor_response,
            5,
            ids
        )
        df = pd.DataFrame(self.all_data)
        print("lenth of Recommandation ==============================>", len(self.Recommandation))
        # print(self.Recommandation)

        df = df.explode('Recommandation')
        df['Recommandation_Name'] = df['Recommandation'].apply(lambda x: x['name'] if isinstance(x, dict) else None)
        df['Recommandation_Date'] = df['Recommandation'].apply(lambda x: x['Date'] if isinstance(x, dict) else None)
        df['Recommandation_Description'] = df['Recommandation'].apply(lambda x: x['Description'] if isinstance(x, dict) else None)
        df = df.drop(columns=['Recommandation'])
        df['Specialites'] = df['Specialites'].apply(lambda x: ', '.join(x) if isinstance(x, list) else None)
        # print(df)
        df.to_csv('Output1.csv', index=False,encoding="utf-8")
        
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