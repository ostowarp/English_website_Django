from django.shortcuts import render
from django.http import HttpResponse

from datetime import timedelta

def calculate_new_interval(response , current_interval):
    if response == "E":
        return current_interval * 3 # افزایش قابل توجه
    elif response == "G":
        return current_interval * 2 # افزاریش متوسط
    elif response == "H":
        return max(1 , current_interval // 2) # کاهش یا حفظ وضعیت
    elif response == "A":
        return max(1 , current_interval // 3) # کاهش قابل توجه 
    else:
        return current_interval # در صورت بروز خطا بازگشت به مقدار قبلی


def dashboard(request):
    return render(request, "dashboard.html" , context={"name":"pouria" , "family":"ostowar"})


def decks(request):
    return HttpResponse("Decks page")


def deck(request, pk):
    return HttpResponse("Single deck page =>" + " " + str(pk))




# make 