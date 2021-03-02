from django.shortcuts import render
from django.views.generic import TemplateView
from django.urls import reverse

from django.http import HttpResponse, HttpResponseRedirect
from django.contrib import messages
from django.contrib.auth.decorators import login_required

from ..models import Location, ConfirmedCase, Coordinate
from ..forms import LocationForm, CaseForm, PatientForm, InfectingVirusForm
from ..cluster import cluster

from datetime import date, timedelta

import numpy as np
import json
import requests

# Create your views here.

# @login_required(login_url='application:login_page')
class homePage(TemplateView):
    template_name = "index.html"

# @login_required(login_url='application:login_page')
def logout(request):
    logout(request)


# @login_required(login_url='application:login_page')
def case_list(request):
    queryset = ConfirmedCase.objects.all()
    context = {
        "case_list": queryset
    }

    return render(request, "case_list.html", context)


def create_location(request):
    form = LocationForm(request.POST or None)

    if form.is_valid():
        form.save()
        form = LocationForm()
        message = "Record successfully created."
    else:
        message = ""

    context = {
        'location_form': form,
        'location_message': message
    }

    return render(request, 'create_location.html', context)


def create_case(request):
    form = CaseForm(request.POST or None)

    if form.is_valid():
        form.save()
        form = CaseForm()
        message = "Record successfully created."
    else:
        message = ""

    context = {
        'case_form': form,
        'case_message': message
    }

    return render(request, 'create_case.html', context)

def create_patient(request):
    form = PatientForm(request.POST or None)

    if form.is_valid():
        form.save()
        form = PatientForm()
        message = "Record successfully created."
    else:
        message = ""

    context = {
        'patient_form': form,
        'patient_message': message
    }
    return render(request, "create_patient.html", context)

def create_virus(request):
    form = InfectingVirusForm(request.POST or None)

    if form.is_valid():
        form.save()
        form = InfectingVirusForm()
        message = "Record successfully created."
    else:
        message = ""

    context = {
        'virus_form': form,
        'virus_message': message
    }
    return render(request, "create_virus.html", context)

# @login_required(login_url='application:login_page')
def get_geodata(request):
    #form = CaseForm(None)

    # get location name data from geodataForm
    data = request.POST.dict()
    location = data.get("location")
    selected_location_index = data.get("selected_location") # for multiple locations

    try:
        selected_location_index = int(selected_location_index)
    except:
        selected_location_index = 0

    if (request.POST):

        # Error for no input
        if len(location) == 0:
            # messages.error(request, 'Please input a location name.')
            # return HttpResponseRedirect(reverse('application:create_case'))

            message = 'Please input a location name.'

            context = {
                #'case_form': form,
                'geodata_message': message
            }
            return render(request, 'index.html', context)

        # print(location)
        query = "https://geodata.gov.hk/gs/api/v1.0.0/locationSearch?q={value}".format(
            value=location)

        response = requests.get(query)
        response_dict = json.loads(response.text)

        # check search keyword match
        name_eng = (response_dict[0]['nameEN']).lower()
        name_chi = response_dict[0]['nameZH']

        # Single match or selected from multiple locations
        if (name_chi == location) or (name_eng == location) or selected_location_index != 0:
            print("match")

            if (selected_location_index > 0):
                index = selected_location_index - 1
            else:
                index = 0

            context = {
                #'case_form': form,
                'location': location,
                'x': response_dict[index]['x'],
                'y': response_dict[index]['y'],
                # 'addressZH': response_dict[0]['addressZH'],
                # 'nameZH': response_dict[0]['nameZH'],
                # 'nameEN': response_dict[0]['nameEN'],
                # 'addressEN': response_dict[0]['addressEN']
            }

        # Multiple match
        else:
            print("not match")

            response_list = []
            # get top 5 results
            for i in range(0, len(response_dict)):
                response_list.append(response_dict[i])

            context = {
                #'case_form': form,
                'location': location,
                'range': 5,
                'geodata_list': response_list
            }

        return render(request, 'index.html', context)

    else:
        context = {
            #'case_form': form,
            'location': location,
        }

        return render(request, 'index.html', context)


# @login_required(login_url='application:login_page')
def create_coord(request):
    form = CaseForm(None)

    # get coord data from coordForm
    if (request.POST):
        data = request.POST.dict()

        x = int(float(data.get("geo_x")))
        y = int(float(data.get("geo_y")))

        coordinate = Coordinate(
            x=x, y=y
        )

        # if there is a matching location in database
        if Coordinate.objects.filter(x=x).exists() and Coordinate.objects.filter(y=y).exists():
            message = "Record already exists in database."
        else:
            try:
                coordinate.save()
                message = "Record successfully created."
            except Exception as error:
                print(error)
                message = error

        context = {
            'case_form': form,
            'coord_message': message
        }

        return render(request, 'index.html', context)

    else:
        return render(request, 'index.html')

def cluster_view(request):

# @login_required(login_url='application:login_page')
# def create_case(request):
#     form = CaseForm(request.POST or None)

    res = {}
    if(request.POST):
        data = request.POST.dict()
        # print("Location.objects.values()")
        confirm = list(ConfirmedCase.objects.values('case_number','date','location'))
        location = list(Location.objects.values('location_id','grid_coordinates'))
        
        locationDict={}
        for i in location:
            locationDict[i['location_id']] = i['grid_coordinates']
        for i in confirm:
            if(i['location'] in locationDict):
                i['location'] = locationDict[i['location']]
        coordinates = list(Coordinate.objects.values('x','y'))
        print(coordinates)
        print(location)
        print(confirm)
        for i in confirm:
            index = i["location"]
            i["location"] = Coordinate.objects.values('x', 'y').get(pk=index)
            d0 = date(2020, 1, 1)
            d1 = i['date']
            day = i['date'] - d0
            i['date'] = day.days
        clusters = []
        for i in confirm:
            temp = [i['location']['x'],i['location']['y'],i['date'],int(i['case_number'])]
            clusters.append(temp)
        clusters = np.array(clusters)
        res = cluster(clusters, int(data['distance']), int(data['time']), int(data['clusterSize']))
        res2 = res['clustres']
        for clust in res2:
            for pt in clust['cluster']:
                days = int(pt['day'])
                start = date(2020,1,1)
                delta = timedelta(days)
                offset = start + delta
                loc_name = Location.objects.filter(grid_coordinates__x = pt['x'], grid_coordinates__y = pt['y']).values('location_name')
                pt['loc'] = loc_name[0]['location_name'];
                pt['day'] = offset
            
    context = {
        'clust' : res
    }

    return render(request, 'cluster_view.html', context)
# @login_required(login_url='application:login_page')
# def create_case(request):
#     form = CaseForm(request.POST or None)
