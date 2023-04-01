from django.shortcuts import render, get_object_or_404
from django.http import HttpResponse
from django.views.generic import TemplateView
import requests
from bs4 import BeautifulSoup
import urllib.request as urllib
import sumy
from sumy.parsers.plaintext import PlaintextParser
from sumy.nlp.tokenizers import Tokenizer
from sumy.summarizers.lsa import LsaSummarizer as Summarizer
from sumy.nlp.stemmers import Stemmer
from sumy.utils import get_stop_words

from politicians.models import City, Department, Politician

LANGUAGE = "english"
SENTENCES_COUNT = 10

# # Create your views here.
# def index(request):
#     return HttpResponse("Local Politician Data Aggregator.")

#########################
#    Display Homepage   #
#########################

def homepage(request):
    return render(request, 'index.html')

#########################
#    Display FAQ        #
#########################

def faq(request):
    return render(request, 'faq.html')

#############################################################
# Get politician's information from their website url input #
# Campaign Link must be manually input into database....... #
#############################################################
govLink, phone, email, fullAddress, title, district, dateElected, bio, party, atLarge = "", "","", "","", "","", "", "", ""

def get_politician_info(request, name):
    inputName = name.replace('-', ' ').strip().title()
    get_object_or_404(Politician, name__exact=inputName)
    if request.method == "GET":
        govLink = Politician.objects.get(name=inputName).gov_link
        page = urllib.urlopen(govLink)
        soup = BeautifulSoup(page, "html.parser") #Parse

        #extract phone and email info into an array
        allSideInfo = soup.find_all("span", class_="sb-d")
        listInfo = [x for x in allSideInfo]
        #phone
        if allSideInfo is not None:
            phone = listInfo[0].text
            if phone != Politician.objects.get(name=inputName).phone:
                obj, created = Politician.objects.update_or_create(
                    name=inputName,
                    defaults={"phone": phone}
                )
        #email
        if allSideInfo is not None:
            email = listInfo[1].find("a")["href"][7:].lower()
            if email != Politician.objects.get(name=inputName).email:
                obj, created = Politician.objects.update_or_create(
                    name=inputName,
                    defaults={"email": email}
                )
        #full title
        title = soup.find("div", attrs={"class":"person-profile-position-title"}).text
        #district
        if title is not None:
            districtIndex = title.find("District")
            atLargeIndex = title.find("At-Large")
            if districtIndex != -1:
                district = title[districtIndex:].strip()
                if district != Politician.objects.get(name=inputName).district or title != Politician.objects.get(name=inputName).title:
                    title = title[:districtIndex-2].strip()
                    obj, created = Politician.objects.update_or_create(
                        name=inputName,
                        defaults={"district": district, "title": title}
                    )
            #technically atLarge but all share under district column
            if atLargeIndex != -1:
                atLarge = title[atLargeIndex:].strip()
                if atLarge != Politician.objects.get(name=inputName).district or title != Politician.objects.get(name=inputName).title:
                    title = title[:atLargeIndex-2].strip()
                    obj, created = Politician.objects.update_or_create(
                        name=inputName,
                        defaults={"district": atLarge, "title": title}
                    )
        
        #full address
        addresses = soup.find("div", class_="addr-l")
        if addresses is not None:
            addressArray = addresses.find_all("span", recursive=False)
            fullAddress = soup.find("div", class_="addr-a").text + " "
            for address in addressArray:
                fullAddress += address.text + " "
            if fullAddress != Politician.objects.get(name=inputName).address:
                obj, created = Politician.objects.update_or_create(
                    name=inputName,
                    defaults={"address": fullAddress}
                )

        #extract party and year elected
        pyAllInfo = soup.find_all("div", class_="dl-d")
        pyListInfo = [x for x in pyAllInfo]
        #party
        if pyAllInfo is not None:
            party = pyListInfo[1].text.strip()
            if party != Politician.objects.get(name=inputName).party:
                obj, created = Politician.objects.update_or_create(
                    name=inputName,
                    defaults={"party": party}
                )
        #year elected
        if pyAllInfo is not None:
            dateElected = pyListInfo[0].text.strip()
            if dateElected != Politician.objects.get(name=inputName).date_elected:
                obj, created = Politician.objects.update_or_create(
                    name=inputName,
                    defaults={"date_elected": dateElected}
                )
        #biography
        bio = soup.find("div", attrs={"person-profile-bio"}).text
        parser = PlaintextParser.from_string(bio, Tokenizer(LANGUAGE))
        stemmer = Stemmer(LANGUAGE)

        summarizer = Summarizer(stemmer)
        summarizer.stop_words = get_stop_words(LANGUAGE)
        bioSum = ""
        for sentence in summarizer(parser.document, SENTENCES_COUNT):
            bioSum += str(sentence) + " "
        if bio != Politician.objects.get(name=inputName).biography:
            obj, created = Politician.objects.update_or_create(
                name=inputName,
                defaults={"biography": bioSum}
            )

        #extract image
        image = soup.find("div", class_="person-profile-photo").find("img")
        image = "https://www.boston.gov" + image['src']
        if image != Politician.objects.get(name=inputName).image:
            obj, created = Politician.objects.update_or_create(
                name=inputName,
                defaults={"image": image}
            )

        return render(request, "politician.html", { #render to the index.html with the contents
            "name": inputName,
            "district": Politician.objects.get(name=inputName).district,
            "title": Politician.objects.get(name=inputName).title,
            "bio": Politician.objects.get(name=inputName).biography,
            "phone": Politician.objects.get(name=inputName).phone,
            "email": Politician.objects.get(name=inputName).email,
            "dateElected": Politician.objects.get(name=inputName).date_elected,
            "address": Politician.objects.get(name=inputName).address,
            "party": Politician.objects.get(name=inputName).party,
            "image": Politician.objects.get(name=inputName).image,
        })
    return render(request, "error.html")

###########################################################
# Politician Dropdown Menu                                #
###########################################################
def dropdown(request):
    check_council_info(request) #check if council info is up to date
    if request.method == "GET":
        #pulling names from db and then storing into list for dropdown menu aspect.
        names, splitNames = [], []
        allNames = Politician.objects.values("name")
        for name in allNames:
            names.append(name['name'].strip())
        splitNames = [val.replace(" ", "-") for val in names]
        #pulling the ids from db for dropdown menu url
        allID = Politician.objects.values("id")
        ids = []
        for id in allID:
            ids.append(id['id'])
        #pulling links from db and then storing into list for dropdown menu aspect.
        links = []
        allLinks = Politician.objects.values("gov_link")
        for link in allLinks:
            links.append(link['gov_link'].strip())
        zipped = zip(names, links, splitNames, ids)
        return render(request, "index.html", {
            "zipped": zipped})
    return render(request, "error.html")

###########################################################
# Populate cities                                         #
###########################################################

def populate_cities(request):
    if request.method == "GET":
        citiesLink = "link for cities"
        page = urllib.urlopen(citiesLink)
        soup = BeautifulSoup(page, "html.parser") #Parse
        #Get name of the cities
        main = soup.find("section", attrs={"id":"content"})
        
        for name, link in zip(names, links):
            obj, created = Politician.objects.get_or_create(
                name=name.text.strip(),
                
            )
        return render(request, "index.html")
    return render(request, "error.html")

###########################################################
# Get departments from the boston.gov website             #
###########################################################

def get_departments(request, name):
    inputName = name.replace('-', ' ').strip()
    get_object_or_404(City, name__exact=inputName)
    if request.method == "GET":
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
                    city_id = City.objects.get(name=inputName).name
                )
    return render(request, "test.html")

###########################################################
# Get mayor info then call into check_council_info to     #
# store into the database                                 #
###########################################################

def get_mayor(request):
    if request.method == "GET":
        mayorLink = "https://www.boston.gov/departments/mayors-office/michelle-wu"
        page = urllib.urlopen(mayorLink)
        soup = BeautifulSoup(page, "html.parser")

        #biography
        bio = soup.find("div", attrs={"person-profile-bio"}).text
        parser = PlaintextParser.from_string(bio, Tokenizer(LANGUAGE))
        stemmer = Stemmer(LANGUAGE)

        summarizer = Summarizer(stemmer)
        summarizer.stop_words = get_stop_words(LANGUAGE)
        bioSum = ""
        for sentence in summarizer(parser.document, SENTENCES_COUNT):
            bioSum += str(sentence) + " "

        #title
        title = soup.find("div", class_="person-profile-position-title").text

        #extract image
        image = soup.find("div", class_="person-profile-photo").find("img")
        image = "https://www.boston.gov" + image['src']

        #name
        name = soup.find("h1", class_="person-profile-display-name").text.strip()

        #extract phone and email info into an array
        allSideInfo = soup.find_all("span", class_="sb-d")
        listInfo = [x for x in allSideInfo]
        #phone
        phone = listInfo[0].text
        #email
        email = listInfo[1].find("a")["href"][7:].lower()

        #full address
        addresses = soup.find("div", class_="addr-l")
        addressArray = addresses.find_all("span", recursive=False)
        fullAddress = soup.find("div", class_="addr-a").text + " "
        for address in addressArray:
            fullAddress += address.text + " "
        
        #extract party and year elected
        pyAllInfo = soup.find_all("div", class_="dl-d")
        pyListInfo = [x for x in pyAllInfo]

        #date elected
        dateElected = pyListInfo[0].text.strip()
        print(dateElected)

        #party
        party = pyListInfo[1].text.strip()


        obj, created = Politician.objects.get_or_create(
            name=name,
            biography=bioSum,
            gov_link=mayorLink,
            title=title,
            image=image,
            date_elected=dateElected,
            address=fullAddress,
            phone=phone,
            email=email,
            party=party
        )


###########################################################
# Get city council information and adds to database.      #
###########################################################

def check_council_info(request):
    get_mayor(request)
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
                name=name.text.strip(),
                gov_link="https://www.boston.gov" + link["href"]
            )
    return render(request, "index.html")