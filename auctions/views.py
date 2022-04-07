from django import forms
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.db import IntegrityError
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render
from django.urls import reverse

from .models import User, Listing, Category, Comment, Bid
# from .utils import catchoices #, valid_url_mimetype, image_exists

class NewLstForm(forms.Form):
    name = forms.CharField(max_length=64, label="Title: ", 
        widget=forms.TextInput(attrs={"class":"InlineInp"}))
    description = forms.CharField(label="Description:",
        widget=forms.Textarea())
    startbid = forms.DecimalField(
        label="Start bid: $",
        min_value=1,
        max_digits=10
        )
    imgurl = forms.URLField(required=False,
        label="Image URL: ",
        help_text="Image size: from 100x100"
        )
    category = forms.ChoiceField(choices=[(0, 'Choose a category')])

    def __init__(self, *args, **kwargs):
        super(NewLstForm, self).__init__(*args, **kwargs)
        self.fields['category'].choices += [(category.pk, category.name) for category in Category.objects.all()]
        self.fields['category'].choices[1:] = sorted(self.fields['category'].choices[1:], key=lambda a: a[1])



class NewBidForm(forms.Form):
    bidvalue = forms.DecimalField(
        label="Your bid: $",
        min_value=1,
        max_digits=10
        )



class NewComForm(forms.Form):
    text = forms.CharField(widget=forms.Textarea())



def index(request):
    actlst = Listing.objects.filter(active=True)
    return render(request, "auctions/index.html",{
        "actlst": actlst,
        "lDescMax": 300,
        "lTitMax": 25
    })


def login_view(request):
    if request.method == "POST":

        # Attempt to sign user in
        username = request.POST["username"]
        password = request.POST["password"]
        user = authenticate(request, username=username, password=password)

        # Check if authentication successful
        if user is not None:
            login(request, user)
            return HttpResponseRedirect(reverse("index"))
        else:
            return render(request, "auctions/login.html", {
                "message": "Invalid username and/or password."
            })
    else:
        return render(request, "auctions/login.html")


def logout_view(request):
    logout(request)
    return HttpResponseRedirect(reverse("index"))


def register(request):
    if request.method == "POST":
        username = request.POST["username"]
        email = request.POST["email"]

        # Ensure password matches confirmation
        password = request.POST["password"]
        confirmation = request.POST["confirmation"]
        if password != confirmation:
            return render(request, "auctions/register.html", {
                "message": "Passwords must match."
            })

        # Attempt to create new user
        try:
            user = User.objects.create_user(username, email, password)
            user.save()
        except IntegrityError:
            return render(request, "auctions/register.html", {
                "message": "Username already taken."
            })
        login(request, user)
        return HttpResponseRedirect(reverse("index"))
    else:
        return render(request, "auctions/register.html")


# Create a new listing
@login_required
def newlisting(request):
    if request.method == "POST":
        form = NewLstForm(request.POST)
        if form.is_valid():
            lst = Listing(
                name = form.cleaned_data["name"],
                description = form.cleaned_data["description"],
                owner = request.user,
                startbid = form.cleaned_data["startbid"],
                curprice = form.cleaned_data["startbid"]
            )
            imgurl = form.cleaned_data["imgurl"]
            if not imgurl == '' or imgurl == None:
                #if valid_url_mimetype(imgurl,):
                lst.image = imgurl

            category = form.cleaned_data["category"]
            if not category == '0':
                lst.category = Category.objects.get(pk=int(category))

            lst.save()
            return HttpResponseRedirect("/")
        else:
            return render(request, "auctions/newlist.html", {
                "form": form
            })
    else:
        return render(request, "auctions/newlist.html", {
            "form": NewLstForm()
        })
            
        

# Review a listing
def listingreview(request, lstpk):

    lst = Listing.objects.get(pk=lstpk)

    nBids = len(lst.listbids.all())

    if lst.watchedby.filter(pk=request.user.pk):
        isInWL=True
    else:
        isInWL=False

    comments = lst.listcomments.all()

    if request.method == "POST": # Make some action with the listing
        if "Place Bid" in request.POST: # NewBid form submitted
            bidForm = NewBidForm(request.POST)
            if bidForm.is_valid() and (bidForm.cleaned_data["bidvalue"] > lst.curprice
                or (bidForm.cleaned_data["bidvalue"] == lst.curprice) and nBids == 0):
                bid = Bid(amount=int(bidForm.cleaned_data["bidvalue"]), # Check for the bid validity
                    bidder=request.user,
                    bidlisting=lst
                    )
                bid.save()

                if not lst.curbid == None:
                    prevbid = lst.curbid
                    prevbid.bitten = True
                    prevbid.save()

                lst.curprice = bid.amount
                lst.curbid = bid
                lst.save()

                return render(request, "auctions/lstreview.html", {
                        "lst": lst,
                        "user": request.user,
                        "formNB": NewBidForm(),
                        "formNC": NewComForm(),
                        "nBids": nBids + 1,
                        "isInWL": isInWL,
                        "comments": comments
                    })
            else: # Not valid
                return render(request, "auctions/lstreview.html", {
                        "lst": lst,
                        "user": request.user,
                        "formNB": NewBidForm(request.POST),
                        "formNC": NewComForm(),
                        "nBids": nBids,
                        "isInWL": isInWL,
                        "comments": comments,
                        "invBidMes": "Bid should be greater than the current price! First bid can be equal to the current price."
                    })
        elif "Add comment" in request.POST: # NewCom form is submitted
            comForm = NewComForm(request.POST)
            if comForm.is_valid():
                com = Comment(text=comForm.cleaned_data["text"],
                    user=request.user,
                    listing=lst
                    )
                com.save()
                return render(request, "auctions/lstreview.html", {
                        "lst": lst,
                        "user": request.user,
                        "formNB": NewBidForm(),
                        "formNC": NewComForm(),
                        "nBids": nBids,
                        "isInWL": isInWL,
                        "comments": comments
                    })
        elif "Close Listing" in request.POST: # We close the listing
            
            lst.active = False
            lst.save()

            return render(request, "auctions/lstreview.html", {
                    "lst": lst,
                    "user": request.user,
                    "formNB": NewBidForm(),
                    "formNC": NewComForm(),
                    "nBids": nBids,
                    "isInWL": isInWL,
                    "comments": comments
                })
        else: # Unlikely - but - unknown form submission
            return render(request, "auctions/debug.html",{
                "ErrMSG": "Unknown Form!"
            })
    else: # Request is GET - just show the listing
        return render(request, "auctions/lstreview.html", {
            "lst": lst,
            "user": request.user,
            "formNB": NewBidForm(),
            "formNC": NewComForm(),
            "nBids": nBids,
            "isInWL": isInWL,
            "comments": comments
        })

@login_required
# Place / remove the current listing to / from the watchlist
def wlswitch(request, lstpk):
    lst = Listing.objects.get(pk=lstpk)
    if lst.watchedby.filter(pk=request.user.pk):
        lst.watchedby.remove(request.user)
    else:
        lst.watchedby.add(request.user)
    
    return HttpResponseRedirect("/review/" + lstpk)

@login_required
# Different users lists
def mylists(request, listType):
    if listType == "WatchList":
        listings = request.user.mywatchings.all()
    elif listType == "MyListings":
        listings = request.user.mylistings.all()
    else:
        return render(request, "auctions/debug.html", {
            "ErrMSG": "Unknown listType!"
        })
    
    actListings = listings.filter(active=True)
    closedListings = listings.filter(active=False)

    return render(request, "auctions/mylists.html",{
        "listType": listType,
        "actListings": actListings,
        "closedListings": closedListings
    })

# List all listings which belong to the chosen category
def cat(request, catpk):
    cat = Category.objects.get(pk=catpk)
    listings = cat.catlistings.all()
    actListings = listings.filter(active=True)
    closedListings = listings.filter(active=False)
    return render(request, "auctions/cat.html",{
        "catname": cat.name,
        "actListings": actListings,
        "closedListings": closedListings
    })