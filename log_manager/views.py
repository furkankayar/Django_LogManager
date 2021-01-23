from django.http import response
from django.shortcuts import render
from .models import log_records



def log_stream(request):
    if not request.is_ajax():
        return response.HttpResponseBadRequest("Only Ajax requests are accepted.")

    if request.method != 'POST':
        return response.HttpResponseNotAllowed(request.method)

    search_str = request.POST.get("search")
    aggregates = []
    if search_str != "":
        aggregates.append({
            "$match": {"$text": {"$search": search_str}}
        })


    last_requests = log_records.aggregate(aggregates + [
        {
            "$sort": {"time": -1}
        },
        {
            "$limit": 100
        },
        {
            "$project": {"_id": 0}
        }
    ])

    data = {
        "last_requests": list(last_requests)
    }

    return response.JsonResponse(data)


def http_method_pie():
    http_method_count = log_records.aggregate([{
        "$group": {
            "_id": {"$toUpper": "$http_method"},
            "count": {"$sum": 1}
        }
    }])

    ids = []
    counts = []
    table_items = []
    for item in http_method_count:
        ids.append(item["_id"])
        counts.append(item["count"])
    suspicious_counter = 0
    real_ids = []
    real_counts = []
    for i in range(0, len(ids)):
        if ids[i] not in ["PUT", "POST", "PATCH", "DELETE", "GET"]:
            suspicious_counter += counts[i]
            continue
        real_ids.append(ids[i])
        real_counts.append(counts[i])
        table_items.append({
            'method': ids[i],
            'count': counts[i],
            'percentage': round(counts[i]/sum(counts)*100, 2)
        })

    real_ids.append("SUSPICIOUS")
    real_counts.append(suspicious_counter)
    table_items.append({
        'method': "SUSPICIOUS",
        'count': suspicious_counter,
        'percentage': round(suspicious_counter/sum(counts)*100, 2)
    })

    return {
        "ids": real_ids if len(real_ids) != 0 else [], 
        "counts": real_counts if len(real_counts) != 0 else [],
        "table_items": table_items if len(table_items) != 0 else []  
    }


def status_code_pie():
    status_code_count = log_records.aggregate([{
        "$group": {
            "_id": {"$toUpper": "$status_code"},
            "count": {"$sum": 1}
        }
    }])

    ids = []
    counts = []
    table_items = []
    for item in status_code_count:
        ids.append(item["_id"])
        counts.append(item["count"])
    for i in range(0, len(ids)):
        table_items.append({
            'method': ids[i],
            'count': counts[i],
            'percentage': round(counts[i]/sum(counts)*100, 2)
        })


    return {
        "ids": ids if len(ids) != 0 else [], 
        "counts": counts if len(counts) != 0 else [],
        "table_items": table_items if len(table_items) != 0 else []  
    }



def requests_month_bar(year = 2016, month = 1):
    requests_month = log_records.aggregate([
        {
            "$project":{
                "year": {"$year": "$time"},
                "month": {"$month": "$time"},
                "day": {"$dayOfMonth": "$time"}
            },
        },
        {
            "$match": {
                "year": int(year), 
                "month": int(month)
            },
        },
        {
            "$group": {
                "_id": "$day",
                "count": {"$sum": 1}
            },
        },
        {
            "$sort": {
                "_id": 1
            }
        }
    ])

    ids = []
    counts = []
    for item in requests_month:
        ids.append(item["_id"])
        counts.append(item["count"])
    return {
        "ids": ids if len(ids) != 0 else [], 
        "counts": counts if len(counts) != 0 else []
    }


def request_month(request):
    if not request.is_ajax():
        return response.HttpResponseBadRequest("Only Ajax requests are accepted.")

    if request.method != 'POST':
        return response.HttpResponseNotAllowed(request.method)

    year = request.POST.get("year")
    month = request.POST.get("month")

    return response.JsonResponse(requests_month_bar(year=year, month=month))


def requested_resource_bar():
    requested_resources = log_records.aggregate([
        {
            "$group": {
                "_id": "$requested_resource",
                "count": {"$sum": 1}
            }
        },
        {
            "$sort": {
                "count": -1
            }
        },
        {
            "$limit": 10
        }
    ])

    ids = []
    counts = []
    for item in requested_resources:
        ids.append(item["_id"])
        counts.append(item["count"])
    
    return {
        "ids": ids if len(ids) != 0 else [], 
        "counts": counts if len(counts) != 0 else []
    }


def index(request):
    
    if not request.user.can_access_log_manager and not request.user.is_superuser:
        return response.HttpResponseForbidden("You are not allowed to access this page.")

    requested_resource_bar()
    return render(request, "index.html", {
        "http_method_pie": http_method_pie(),
        "requested_resources_bar": requested_resource_bar(),
        "requests_month_bar": requests_month_bar(),
        "status_code_pie": status_code_pie()
    })