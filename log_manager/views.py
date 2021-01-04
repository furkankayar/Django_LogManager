from django.db.models.aggregates import Count
from django.http import response
from django.shortcuts import render
from .models import LogRecord
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

    for i in range(0, len(ids)):
        if ids[i] == "":
            ids[i] = "UNDEFINED"
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
    
    requested_resource_bar()
    return render(request, "index.html", {
        "http_method_pie": http_method_pie(),
        "requested_resources_bar": requested_resource_bar()
    })