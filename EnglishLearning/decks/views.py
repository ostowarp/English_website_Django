from django.shortcuts import render
from django.http import HttpResponse
from django.shortcuts import redirect

# import Form:
from .form import DeckForm , FlashCardForm

# import database:
from .models import Deck


def createDeck(request):
    form = DeckForm()
    if request.method == "POST":
        form = DeckForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect("dashboard")
    context = {"form": form}
    return render(request, "deck_form.html", context)



from datetime import timedelta


def calculate_new_interval(response, current_interval):
    if response == "E":
        return current_interval * 3  # افزایش قابل توجه
    elif response == "G":
        return current_interval * 2  # افزاریش متوسط
    elif response == "H":
        return max(1, current_interval // 2)  # کاهش یا حفظ وضعیت
    elif response == "A":
        return max(1, current_interval // 3)  # کاهش قابل توجه
    else:
        return current_interval  # در صورت بروز خطا بازگشت به مقدار قبلی


# print(Deck.objects.all())
def dashboard(request):
    context = {"decks": Deck.objects.all()}
    return render(request, "dashboard.html", context)


def decks(request):
    return HttpResponse("Decks page")


def deck(request, pk):
    deck = Deck.objects.get(id=pk)
    # related name: flashcards
    subdeck = deck.subdecks.first()
    context = {"name":deck , "subdeck":subdeck ,"flashcards": deck.flashcards.all()}
    return render(request, "singledeck.html", context)


# make
