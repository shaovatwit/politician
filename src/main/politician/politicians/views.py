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
#############################################################

def get_politician_info(request, politician_id):
    if request.method == "GET":
        govLink = Politician.objects.get(politician_id=politician_id).gov_link
        # print(govLink)
        page = urllib.urlopen(govLink)
        soup = BeautifulSoup(page, "html.parser") #Parse

        #check if content is in database, if not then push to database and then pull from database to display
        # if politician columns not in database then
        #     get or create add them
        # render from database to webpage.
        name = soup.find(class_="person-profile-display-name").text
        allSideInfo = soup.find_all("span", class_="sb-d")
        listInfo = [x for x in allSideInfo]
        phone = listInfo[0].text
        email = listInfo[1].find("a")["href"][7:]
        title = soup.find("div", attrs={"class":"person-profile-position-title"}).text

        #if statement to check if district in text and then extract that word + the #

        bio = soup.find("div", attrs={"person-profile-bio"}).text

        obj, created = Politician.objects.update_or_create(
            politician_id=politician_id,
            biography=bio,
            email=email,
            phone=phone,
            defaults={
                "biography":bio,
                "email":email,
                "phone":phone
            }
        )

        return render(request, "test.html", { #render to the index.html with the contents
            #"name": name
            "name": name,
            "title": title,
            "bio": bio,
            "phone": phone
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