from django.shortcuts import render
from django.http import HttpResponse
from django.views.generic import TemplateView
import requests
from bs4 import BeautifulSoup

from . import models

# Create your views here.
def index(request):
    return HttpResponse("Local Politician Data Aggregator.")

#############################################################
# Display Homepage #
#############################################################

def homepage(request):
    return render(request, 'main.html')

#############################################################
# Get politician's information from their website url input #
#############################################################

def get_politician_info(request, politician_id):
    #Check if politician_id exists in the database... if so, get otherwise post
    if request.method == "POST":
        url = request.POST.get('url') #Get URL Input
        req = request.get(url) #Make Request
        web_s = req.text #Website of the request
        soup = BeautifulSoup(web_s, "html.parser") #Parse
        #Get name of the politician.
        #Politician wishes for their citizens?

        return render(request, "index.html", { #render to the index.html with the contents
            #"name": name
        })
    return render(request, "index.html")

###########################################################
# Get city information and searches database for the      #
# politician in that area. Then fetches the url from the  #
# database to scrape the data                             #
###########################################################

def get_city(request, city_id):
    if request.method == "POST":
        url = request.POST.get('boston.gov site')
        req = request.get(url)
        web_s = req.text
        soup = BeautifulSoup(web_s, "html.parser")

        #Get number of councilors

        return render(request, "whateverpage.html", {
            #counsilors
        })
    return render(request, "wateverpage.html")