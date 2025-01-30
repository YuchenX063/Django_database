from django.shortcuts import render
from django.http import HttpResponse
from django.http import Http404
from django.shortcuts import render, get_object_or_404
from .models import Church, Person, Church_Person, Small_Church, Church_Church, Small_Church_Person
from django.core.paginator import Paginator
from itertools import chain

# Create your views here.

def index(request):
    church_name = request.GET.get('church_name')
    person_name = request.GET.get('person_name')
    place_name = request.GET.get('place_name')
    language = request.GET.get('language')

    church_id = request.GET.get('church_instID')
    person_id = request.GET.get('person_persID')

    year = request.GET.get('year')
    diocese = request.GET.get('diocese')
    
    church_list = Church.objects.all()
    small_church_list = Small_Church.objects.all()
    person_list = Person.objects.all()
    
    if church_name:
        church_list = church_list.filter(instName__icontains=church_name)
        small_church_list = small_church_list.filter(instName__icontains=church_name)
        related_persons = Church_Person.objects.filter(person_church__instName__icontains=church_name).values_list('person', flat=True)
        related_small_church_persons = Small_Church_Person.objects.filter(person_church__instName__icontains=church_name).values_list('person', flat=True)
        person_list_church = person_list.filter(id__in=related_persons)
        person_list_small_church = person_list.filter(id__in=related_small_church_persons)
        person_list = person_list_church | person_list_small_church
    
    if place_name:
        church_list = church_list.filter(city_reg__icontains=place_name)
        small_church_list = small_church_list.filter(city_reg__icontains=place_name)
        related_persons = Church_Person.objects.filter(person_church__city_reg__icontains=place_name).values_list('person', flat=True)
        person_list = person_list.filter(id__in=related_persons)
    
    if diocese:
        church_list = church_list.filter(diocese__icontains=diocese)
        small_church_list = small_church_list.filter(diocese__icontains=diocese)
        related_persons = Church_Person.objects.filter(person_church__diocese__icontains=diocese).values_list('person', flat=True)
        person_list = person_list.filter(id__in=related_persons)
    
    if person_name:
        person_list = person_list.filter(persName__icontains=person_name)
        related_churches = Church_Person.objects.filter(person__persName__icontains=person_name).values_list('person_church', flat=True)
        church_list = church_list.filter(id__in=related_churches)
        small_church_list = small_church_list.filter(id__in=related_churches)
    
    if language:
        church_list = church_list.filter(language__icontains=language)
        small_church_list = small_church_list.filter(language__icontains=language)
        related_persons = Church_Person.objects.filter(person_church__language__icontains=language).values_list('person', flat=True)
        person_list = person_list.filter(id__in=related_persons)

    if church_id:
        church_list = Church.objects.filter(instID=church_id)
        small_church_list = Small_Church.objects.filter(instID=church_id)
        related_persons = Church_Person.objects.filter(person_church__instID__icontains=church_id).values_list('person', flat=True)
        person_list = Person.objects.filter(id__in=related_persons)

    if person_id:  
        person_list = Person.objects.filter(persID=person_id)
        related_churches = Church_Person.objects.filter(person__persID__icontains=person_id).values_list('person_church', flat=True)
        church_list = Church.objects.filter(id__in=related_churches)
        small_church_list = Small_Church.objects.filter(id__in=related_churches)

    if year:
        church_list = church_list.filter(year=year)
        small_church_list = small_church_list.filter(year=year)
        person_list = person_list.filter(year=year)

    church_list = church_list.order_by('instID', 'year')
    small_church_list = small_church_list.order_by('instID', 'year')
    person_list = person_list.order_by('persID', 'year')

    church_combined_list = list(chain(church_list, small_church_list))

    church_paginator = Paginator(church_combined_list, 15)  # Show 15 churches per page
    person_paginator = Paginator(person_list, 15)  # Show 15 persons per page
    
    church_page_number = request.GET.get('church_page')
    person_page_number = request.GET.get('person_page')
    
    church_page_obj = church_paginator.get_page(church_page_number)
    person_page_obj = person_paginator.get_page(person_page_number)
    
    return render(request, 'database/index.html', {
        'church_page_obj': church_page_obj,
        'person_page_obj': person_page_obj,
        'church_name': church_name,
        'person_name': person_name,
        'place_name': place_name
    })

def church_detail(request, instID, year): #query a church by instID and year
    church = Church.objects.filter(instID=instID, year=year).first()
    if church:
        related_persons = Church_Person.objects.filter(person_church=church)
        attending_small_churches = Church_Church.objects.filter(instID=church.instID, year_church=church.year)
        attending_small_churches_details = []
        for attending in attending_small_churches:
            try:
                small_church = Small_Church.objects.get(instID=attending.attendingInstID, year=attending.year_small_church)
                attending_small_churches_details.append({
                    'instID': small_church.instID,
                    'year': small_church.year,
                    'instName': small_church.instName
                })
            except Small_Church.DoesNotExist:
                continue
        return render(request, 'database/church.html', {
            'church': church,
            'related_persons': related_persons,
            'attending_small_churches': attending_small_churches_details
        })
    else:
        try:
            small_church = Small_Church.objects.get(instID=instID, year=year)
            #related_persons = Church_Person.objects.filter(person_church=small_church)
            related_persons = []
            attending_church_name = None
            if small_church.attendingInstID:
                try:
                    attending_church = Church.objects.get(instID=small_church.attendingInstID, year=year)
                    attending_church_name = attending_church.instName
                except Church.DoesNotExist:
                    attending_church_name = "Unknown"
            return render(request, 'database/small_church.html', {
                'church': small_church,
                'related_persons': related_persons,
                'attending_church_name': attending_church_name
            })
        except Small_Church.DoesNotExist:
            return render(request, 'database/does_not_exist.html', {'instID': instID, 'year': year})

def person_detail(request, persID, year): #query a person by persID and year
    person = get_object_or_404(Person, persID=persID, year=year)
    related_churches = Church_Person.objects.filter(person=person)
    return render(request, 'database/person.html', {'person': person, 'related_churches': related_churches})