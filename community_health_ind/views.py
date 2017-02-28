import datetime
from django.shortcuts import render
from django.http import JsonResponse
from collections import OrderedDict

from rest_framework import status
from rest_framework.response import Response

from community_health_ind import models
import community_health_ind.models
import MySQLdb


# Create your views here.
def sample(request, username, pwd):
    # l = ['kishore', 'asdf', 'qwepoiru']
    # dict = OrderedDict()
    # dict['username'] = username
    # dict['pwd'] = pwd
    # dict['one'] = 1
    # dict['twice'] = 2
    # dict['date'] = datetime.datetime.now()
    # return JsonResponse(dict)
    db = MySQLdb.connect(user='root', db='community_data_indicator', passwd='', host='localhost')
    cursor = db.cursor()
    cursor.execute('SELECT count(*) FROM user WHERE username=\'{}\' and password=\'{}\';'.format(username, pwd))
    print('SELECT count(*) FROM user WHERE username=\'{}\' and password=\'{}\';'.format(username, pwd))

    count = [row[0] for row in cursor.fetchall()]
    cursor.close()
    db.close()
    if count[0] == 1:
        return JsonResponse({'loginstatus': True})
    elif count[0] == 0:
        return JsonResponse({'loginstatus': False})
    return JsonResponse({'none': 'none retuened'})


def findCounty(request, countyName):
    print(countyName)
    list = models.County.objects.filter(county_name__iexact=countyName)
    county_id = 1;
    for county in list:
        county_id = county.county_id
        break

    print("county id is {}".format(county_id))
    db = MySQLdb.connect(user='root', db='community_data_indicator', passwd='', host='localhost')
    cursor = db.cursor()
    cursor.execute('SELECT * FROM health_data WHERE county_id={}'.format(county_id))
    names = [row[0] for row in cursor.fetchall()]
    cursor.close()
    db.close()
    return JsonResponse({'names': names})
    # health_data_dict)render(request, 'book_list.html', {'names': names})

    # health_data_list = models.HealthData.objects.filter(county_id__exact=county_id).values()
    # health_data_list = []
    # for dat in models.HealthData.objects.raw("SELECT *FROM health_data WHERE county_id=%d", [int(county_id)]):
    #     health_data_list.append(dat)
    #     print(dat)
    # health_data_dict = dict(health_data_list)
    # return JsonResponse(health_data_dict)


def login(request, usrname, password):
    print(usrname, password)
    try:
        user = models.User.objects.get(username=usrname)
    except community_health_ind.User.DoesNotExist:
        return JsonResponse(status=status.HTTP_404_NOT_FOUND)

    if user.password == password:
        topic = models.HealthTopic.objects.get(htopic_id=user.disease).description
        county = models.County.objects.get(county_id=user.county)

        user_details = {'email': user.username, 'first_name': user.first_name, 'last_name': user.last_name,
                        'mapped_county': county.county_name, 'mapped_county_id': str(county.county_id),
                        'mapped_disease': topic, 'mapped_disease_id': str(user.disease)}
        return JsonResponse(user_details)

    else:
        return Response(status=status.HTTP_401_UNAUTHORIZED)


def findCountyList(request, disease_name, limit=500):
    try:
        mDisease = models.HealthTopic.objects.get(htopic_id=disease_name)
    except Exception as e:
        print("exception raised: does not exist")
        return JsonResponse({'status': 'failure'})
    topic_id = mDisease.htopic_id
    string1 = '''select c.county_name, hd.county_id, hd.htopic_id, h.description, i.description, event_count,
    avg_num_den, measure, percent, mapping_distribution, c.location
    from health_data hd
    inner
    join
    health_topic
    h
    on
    h.htopic_id = hd.htopic_id
    inner
    join
    County
    c
    on
    c.county_id = hd.county_id
    inner
    join
    Indicator
    i
    on
    i.indicator_id = hd.indicator_id
    where
     hd.htopic_id = {} order by hd.county_id limit {};
    '''.format(disease_name, limit)

    db = MySQLdb.connect(user='root', db='community_data_indicator', passwd='', host='localhost')
    cursor = db.cursor()
    cursor.execute(string1)
    result = []
    for row in cursor.fetchall():
        drow = {
            'countyName': row[0],
            'countyId': str(row[1]),
            'diseaseId': str(row[2]),
            'diseaseDescription': row[3],
            'indDescription': row[4],
            'eventCount': str(row[5]),
            'avgNumDen': str(row[6]),
            'measure': row[7],
            'percent': str(row[8]),
            'mappingDist': str(row[9]),
            'location': row[10]
        }
        result.append(drow)
    cursor.close()
    db.close()
    resDict = OrderedDict({
        'status': 'success',
        'result': result
    })
    return JsonResponse(resDict)

def findDiseaseList(request, cnty_name):
    try:
        county_id = models.County.objects.get(county_name=cnty_name).county_id
    except Exception as e:
        print("exception raised: does not exist")
        return JsonResponse({'status': 'failure'})
    string1 = '''select c.county_name, hd.county_id, hd.htopic_id, h.description, i.description, event_count,
    avg_num_den, measure, percent, mapping_distribution, c.location
    from health_data hd
    inner
    join
    health_topic
    h
    on
    h.htopic_id = hd.htopic_id
    inner
    join
    County
    c
    on
    c.county_id = hd.county_id
    inner
    join
    Indicator
    i
    on
    i.indicator_id = hd.indicator_id
    where
     hd.county_id = {};
    '''.format(county_id)

    db = MySQLdb.connect(user='root', db='community_data_indicator', passwd='', host='localhost')
    cursor = db.cursor()
    cursor.execute(string1)
    result = []
    for row in cursor.fetchall():
        drow = {
            'countyName': row[0],
            'countyId': str(row[1]),
            'diseaseId': str(row[2]),
            'diseaseDescription': row[3],
            'indDescription': row[4],
            'eventCount': str(row[5]),
            'avgNumDen': str(row[6]),
            'measure': row[7],
            'percent': str(row[8]),
            'mappingDist': str(row[9]),
            'location': row[10]
        }
        result.append(drow)
    cursor.close()
    db.close()
    resDict = OrderedDict({
        'status': 'success',
        'result': result
    })
    return JsonResponse(resDict)
