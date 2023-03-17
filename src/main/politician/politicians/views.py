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
    #Check if politician_id exists in the database... if so, get otherwise post
    if request.method == "GET":
        govLink = Politician.objects.get(politician_id=politician_id).gov_link
        # print(govLink)
        page = urllib.urlopen(govLink)
        soup = BeautifulSoup(page, "html.parser") #Parse
        #Get name of the politician.
        title = soup.title.string
        #Politician wishes for their citizens?

        

        return render(request, "index.html", { #render to the index.html with the contents
            #"name": name
            "title": title
        })
    return render(request, "index.html")

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