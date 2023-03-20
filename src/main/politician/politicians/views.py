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
phone, email, fullAddress, title, district, dateElected, bio, party = ""

def get_politician_info(request, politician_id):
    if request.method == "GET":
        govLink = Politician.objects.get(politician_id=politician_id).gov_link
        page = urllib.urlopen(govLink)
        soup = BeautifulSoup(page, "html.parser") #Parse

        # #first and last name
        # name = soup.find(class_="person-profile-display-name").text

        #extract phone and email info into an array
        allSideInfo = soup.find_all("span", class_="sb-d")
        listInfo = [x for x in allSideInfo]
        #phone
        if allSideInfo is not None:
            phone = listInfo[0].text
        if phone != Politician.objects.get(politician_id=politician_id).phone:
            print(phone)
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
            district = title[districtIndex:].strip()
        if district != Politician.objects.get(politician_id=politician_id).district:
            obj, created = Politician.objects.update_or_create(
                politician_id = politician_id,
                defaults={"district": district}
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

        return render(request, "test.html", { #render to the index.html with the contents
            #"name": name
            "district": Politician.objects.get(politician_id=politician_id).district,
            "bio": Politician.objects.get(politician_id=politician_id).biography,
            "phone": Politician.objects.get(politician_id=politician_id).phone,
            "email": Politician.objects.get(politician_id=politician_id).email,
            "dateElected": Politician.objects.get(politician_id=politician_id).date_elected,
            "address": Politician.objects.get(politician_id=politician_id).address,
            "party": Politician.objects.get(politician_id=politician_id).party
        })
    return render(request, "test.html")

###########################################################
# Get city information and searches database for the      #
# politician in that area. Then fetches the url from the  #
# database to scrape the data                             #
###########################################################

def get_city(request, city_id):
    if request.method == "GET":
        # city, created = City.objects.get_or_create(city_id)

        url = request.POST.get('boston.gov site')
        req = request.get(url)
        web_s = req.text
        soup = BeautifulSoup(web_s, "html.parser")

        #Get number of councilors

        return render(request, "city.html", {
            #counsilors
        })
    return render(request, "city.html")

###########################################################
# Get city council information and searches database if   #
# politician exists. Then stores and or updates the info  #
# in the database                                         #
###########################################################

def check_council_info(request):
    #Check if politician_id exists in the database... if so, get otherwise post
    if request.method == "GET":
        govLink = "https://www.boston.gov/departments/city-council"
        page = urllib.urlopen(govLink)
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