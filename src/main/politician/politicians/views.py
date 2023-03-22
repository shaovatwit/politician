from django.shortcuts import render
from django.http import HttpResponse
from django.views.generic import TemplateView
import requests
from bs4 import BeautifulSoup
import urllib.request as urllib

from politicians.models import City, Department, Politician, Office

# # Create your views here.
# def index(request):
#     return HttpResponse("Local Politician Data Aggregator.")

#########################
#    Display Homepage   #
#########################

def homepage(request):
    return render(request, 'index.html')

#############################################################
# Get politician's information from their website url input #
# Campaign Link must be manually input into database....... #
#############################################################
govLink, phone, email, fullAddress, title, district, dateElected, bio, party = "", "","", "","", "","", "", ""

def get_politician_info(request, politician_id, name):
    inputName = name.replace('-', ' ').strip().casefold()
    if request.method == "GET" and inputName == Politician.objects.get(politician_id=politician_id).name.casefold().strip():
        govLink = Politician.objects.get(politician_id=politician_id).gov_link
        page = urllib.urlopen(govLink)
        soup = BeautifulSoup(page, "html.parser") #Parse

        #extract phone and email info into an array
        allSideInfo = soup.find_all("span", class_="sb-d")
        listInfo = [x for x in allSideInfo]
        #phone
        if allSideInfo is not None:
            phone = listInfo[0].text
        if phone != Politician.objects.get(politician_id=politician_id).phone:
            obj, created = Politician.objects.update_or_create(
                politician_id = politician_id,
                defaults={"phone": phone}
            )
        #email
        if allSideInfo is not None:
            email = listInfo[1].find("a")["href"][7:]
        if email != Politician.objects.get(politician_id=politician_id).email:
            obj, created = Politician.objects.update_or_create(
                politician_id = politician_id,
                defaults={"email": email}
            )
        #full title
        title = soup.find("div", attrs={"class":"person-profile-position-title"}).text
        #district
        if title is not None:
            districtIndex = title.find("District")
            district = title[districtIndex+8:].strip()
            title = title[:districtIndex-2].strip()
        if district != Politician.objects.get(politician_id=politician_id).district or title != Politician.objects.get(politician_id=politician_id).title:
            obj, created = Politician.objects.update_or_create(
                politician_id = politician_id,
                defaults={"district": district, "title": title}
            )
        #full address
        addresses = soup.find("div", class_="addr-l")
        if addresses is not None:
            addressArray = addresses.find_all("span", recursive=False)
            fullAddress = soup.find("div", class_="addr-a").text + " "
            for address in addressArray:
                fullAddress += address.text + " "
        if fullAddress != Politician.objects.get(politician_id=politician_id).address:
            obj, created = Politician.objects.update_or_create(
                politician_id = politician_id,
                defaults={"address": fullAddress}
            )

        #extract party and year elected
        pyAllInfo = soup.find_all("div", class_="dl-d")
        pyListInfo = [x for x in pyAllInfo]
        #party
        if pyAllInfo is not None:
            party = pyListInfo[1].text.strip()
        if party != Politician.objects.get(politician_id=politician_id).party:
            obj, created = Politician.objects.update_or_create(
                politician_id = politician_id,
                defaults={"party": party}
            )
        #year elected
        if pyAllInfo is not None:
            dateElected = pyListInfo[0].text.strip()
        if dateElected != Politician.objects.get(politician_id=politician_id).date_elected:
            obj, created = Politician.objects.update_or_create(
                politician_id = politician_id,
                defaults={"date_elected": dateElected}
            )
        #biography
        bio = soup.find("div", attrs={"person-profile-bio"}).text
        if bio is not None and bio != Politician.objects.get(politician_id=politician_id).biography:
            obj, created = Politician.objects.update_or_create(
                politician_id = politician_id,
                defaults={"biography": bio}
            )
            
        #pulling names from db and then storing into list for dropdown menu aspect.
        names, splitNames = [], []
        allNames = Politician.objects.values("name")
        for name in allNames:
            names.append(name['name'].strip())
        splitNames = [val.replace(" ", "-") for val in names]
        #pulling the ids from db for dropdown menu url
        allID = Politician.objects.values("politician_id")
        ids = []
        for id in allID:
            ids.append(id['politician_id'])
        #pulling links from db and then storing into list for dropdown menu aspect.
        links = []
        allLinks = Politician.objects.values("gov_link")
        for link in allLinks:
            links.append(link['gov_link'].strip())
        zipped = zip(names, links, splitNames, ids)

        #extract image
        image = soup.find("div", class_="person-profile-photo").find("img")
        image = "https://www.boston.gov" + image['src']
        print(title)

        return render(request, "politician.html", { #render to the index.html with the contents
            "zipped": zipped,
            "name": Politician.objects.get(politician_id=politician_id).name,
            "district": Politician.objects.get(politician_id=politician_id).district,
            "title": Politician.objects.get(politician_id=politician_id).title,
            "bio": Politician.objects.get(politician_id=politician_id).biography,
            "phone": Politician.objects.get(politician_id=politician_id).phone,
            "email": Politician.objects.get(politician_id=politician_id).email,
            "dateElected": Politician.objects.get(politician_id=politician_id).date_elected,
            "address": Politician.objects.get(politician_id=politician_id).address,
            "party": Politician.objects.get(politician_id=politician_id).party,
            "image": image,
        })
    return render(request, "test2.html")

###########################################################
# Get departments from the boston.gov website             #
###########################################################

def get_departments(request, name, city_id, department_id):
    inputName = name.replace('-', ' ').strip()
    if City.objects.filter(city_id=city_id).first() is None:
        return render(request, "test2.html")
    if request.method == "GET" and inputName == City.objects.get(city_id=city_id).name.casefold().strip():
        deptLink = urllib.urlopen('https://www.boston.gov/departments')

        soup = BeautifulSoup(deptLink, "html.parser")
        main = soup.find("div", class_="b-c")
        allContent = ""
        if main is not None:
            #gets the href of the department links
            links = main.find_all("a", class_="cdd", href=True)
            #gets the department and their numbers
            allContent = main.find_all("div", class_="cdd-d-i")
            deptInfo = []
            for x in allContent:
                leftStrip = x.text.lstrip("\n")
                rightStrip = leftStrip.rstrip("\n")
                deptInfo.append(rightStrip.split("\n"))
            flattened = [val for nest in deptInfo for val in nest]
            departments = flattened[::2]
            deptNum = flattened[1::2]

            #get or create department info
            for dept, num, link in zip(departments, deptNum, links):
                obj, created = Department.objects.get_or_create(
                    name = dept,
                    phone = num[0:13],
                    url = "https://www.boston.gov" + link["href"],
                    city_id = City.objects.get(city_id=city_id).city_id
                )
    return render(request, "test.html")

###########################################################
# Get city council information and adds to database.      #
###########################################################

def check_council_info(request):
    if request.method == "GET":
        councilLink = "https://www.boston.gov/departments/city-council"
        page = urllib.urlopen(councilLink)
        soup = BeautifulSoup(page, "html.parser") #Parse
        #Get name of the councils
        main = soup.find("section", attrs={"id":"content"})
        names = main.find_all("div", attrs={"class":"cdp-t"})
        links = main.find_all("a", attrs={"class":"cdp-l"}, href=True)
        for name, link in zip(names, links):
            obj, created = Politician.objects.get_or_create(
                name=name.text,
                gov_link="https://www.boston.gov" + link["href"]
            )
    return render(request, "test.html")