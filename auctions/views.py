from django.contrib.auth import authenticate, login, logout
from django.db import IntegrityError
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render, redirect
from django.urls import reverse
from django.contrib.auth.decorators import login_required
from datetime import datetime

from .models import User, Watchlist, Listing, Listtotal, Comment, Bid, Auctionclosed

def index(request):
    articles = Listing.objects.all()
    try:
        w = Watchlist.objects.filter(user=request.user.username)
        wcount=len(w)
    except:
        wcount=None
    return render(request, "auctions/index.html",{
        "articles":articles,
        "wcount":wcount
    })

# This function create a new item to be auctioned, 
# a request is made to the object Watchlist.

def createlist(request):
    try:
        w = Watchlist.objects.filter(user=request.user.username)
        wcount=len(w)
    except:
        wcount=None
    return render(request,"auctions/createlist.html",{
        "wcount":wcount
    })


# In this function the items added to the wish list are tracked, 
# a request is made to the object Watchlist

def pagelist(request, username):
    if request.user.username:
        try:
            w = Watchlist.objects.filter(user=username)
            articles = []
            for i in w:
                articles.append(Listing.objects.filter(id=i.listingid))
            try:
                w = Watchlist.objects.filter(user=request.user.username)
                wcount=len(w)
            except:
                wcount=None
            return render(request,"auctions/pagelist.html",{
                "articles": articles,
                "wcount":wcount
            })
        except:
            try:
                w = Watchlist.objects.filter(user=request.user.username)
                wcount=len(w)
            except:
                wcount=None
            return render(request,"auctions/pagelist.html",{
                "articles":None,
                "wcount":wcount
            })
    else:
        return redirect('index')


# This function sends the information of the article that is ready to be created 
# and saved in the database, makes a request to the objects, Listing, Listtotal

def submit(request):
    if request.method == "POST":
        listtable = Listing()
        now = datetime.now()
        dt = now.strftime(" %d %B %Y %X ")
        listtable.owner = request.user.username
        listtable.title = request.POST.get('title')
        listtable.description = request.POST.get('description')
        listtable.price = request.POST.get('price')
        listtable.category = request.POST.get('category')
        if request.POST.get('link'):
            listtable.link = request.POST.get('link')
        else :
            listtable.link = "https://www.pequenomundo.cl/wp-content/themes/childcare/images/default.png"
        listtable.time = dt
        listtable.save()
        all = Listtotal()
        articles = Listing.objects.all()
        for i in articles:
            try:
                if Listtotal.objects.get(listingid=i.id):
                    pass
            except:
                all.listingid=i.id
                all.title = i.title
                all.description = i.description
                all.link = i.link
                all.save()

        return redirect('index')
    else:
        return redirect('index')


def pagelisttotal(request, id):
    try:
        article = Listing.objects.get(id=id)
    except:
        return redirect('index')
    try:
        comments = Comment.objects.filter(listingid=id)
    except:
        comments = None
    if request.user.username:
        try:
            if Watchlist.objects.get(user=request.user.username,listingid=id):
                added=True
        except:
            added = False
        try:
            l = Listing.objects.get(id=id)
            if l.owner == request.user.username :
                owner=True
            else:
                owner=False
        except:
            return redirect('index')
    else:
        added=False
        owner=False
    try:
        w = Watchlist.objects.filter(user=request.user.username)
        wcount=len(w)
    except:
        wcount=None
    return render(request,"auctions/pagelisttotal.html",{
        "i": article,
        "error":request.COOKIES.get('error'),
        "errorgreen":request.COOKIES.get('errorgreen'),
        "comments":comments,
        "added":added,
        "owner":owner,
        "wcount":wcount
    })

# This function sends a comment

def submitct(request, listingid):
    if request.method == "POST":
        now = datetime.now()
        dt = now.strftime(" %d %B %Y %X ")
        c = Comment()
        c.comment = request.POST.get('comment')
        c.user = request.user.username
        c.time = dt
        c.listingid = listingid
        c.save()
        return redirect('pagelisttotal', id=listingid)
    else :
        return redirect('index')

def uploadsubmit(request, listingid):
    current_bid = Listing.objects.get(id=listingid)
    current_bid=current_bid.price
    if request.method == "POST":
        user_bid = int(request.POST.get("bid"))
        if user_bid > current_bid:
            listing_items = Listing.objects.get(id=listingid)
            listing_items.price = user_bid
            listing_items.save()
            try:
                if Bid.objects.filter(id=listingid):
                    bidrow = Bid.objects.filter(id=listingid)
                    bidrow.delete()
                bidtable = Bid()
                bidtable.user=request.user.username
                bidtable.title = listing_items.title
                bidtable.listingid = listingid
                bidtable.bid = user_bid
                bidtable.save()                
            except:
                bidtable = Bid()
                bidtable.user=request.user.username
                bidtable.title = listing_items.title
                bidtable.listingid = listingid
                bidtable.bid = user_bid
                bidtable.save()
            response = redirect('pagelisttotal', id=listingid)
            response.set_cookie('errorgreen','Excellent you are participating in the auction!!',max_age=3)
            return response
        else :
            response = redirect('pagelisttotal', id=listingid)
            response.set_cookie('error','Bid should be greater than current price',max_age=3)
            return response
    else:
        return redirect('index')


# This function adds an item to the watchlist

def addtolist(request, listingid):
    if request.user.username:
        w = Watchlist()
        w.user = request.user.username
        w.listingid = listingid
        w.save()
        return redirect('pagelisttotal', id=listingid)
    else:
        return redirect('index')

# This function removes the item from the watchlist

def removelist(request, listingid):
    if request.user.username:
        try:
            w = Watchlist.objects.get(user=request.user.username, listingid=listingid)
            w.delete()
            return redirect('pagelisttotal',id=listingid)
        except:
            return redirect('pagelisttotal',id=listingid)
    else:
        return redirect('index')

# This function shows the existing categories to search

def categories(request):
    articles = Listing.objects.raw("SELECT * FROM auctions_listing GROUP BY category")
    try:
        w = Watchlist.objects.filter(user=request.user.username)
        wcount=len(w)
    except:
        wcount=None
    return render(request,"auctions/pagecategories.html",{
        "articles": articles,
        "wcount":wcount
    })

# This function selects the category and shows me the existing articles

def category(request,category):
    articlescategory = Listing.objects.filter(category=category)
    try:
        w = Watchlist.objects.filter(user=request.user.username)
        wcount=len(w)
    except:
        wcount=None
    return render(request,"auctions/category.html",{
        "articles":articlescategory,
        "catego":category,
        "wcount":wcount
    })

# This function closes the auction and adds it to the winning user

def endauction(request, listingid):
    if request.user.username:
        try:
            listingrow = Listing.objects.get(id=listingid)
        except:
            return redirect('index')
        cb = Auctionclosed()
        title = listingrow.title
        cb.owner = listingrow.owner
        cb.listingid = listingid
        try:
            bidrow = Bid.objects.get(listingid=listingid, bid=listingrow.price)
            cb.winner = bidrow.user
            cb.winprice = bidrow.bid
            cb.save()
            bidrow.delete()
        except:
            cb.winner = listingrow.owner
            cb.winprice = listingrow.price
            cb.save()
        try:
            if Watchlist.objects.filter(listingid=listingid):
                watchrow = Watchlist.objects.filter(listingid=listingid)
                watchrow.delete()
            else:
                pass
        except:
            pass
        try:
            crow = Comment.objects.filter(listingid=listingid)
            crow.delete()
        except:
            pass
        try:
            brow = Bid.objects.filter(listingid=listingid)
            brow.delete()
        except:
            pass
        try:
            cblist=Auctionclosed.objects.get(listingid=listingid)
        except:
            cb.owner = listingrow.owner
            cb.winner = listingrow.owner
            cb.listingid = listingid
            cb.winprice = listingrow.price
            cb.save()
            cblist=Auctionclosed.objects.get(listingid=listingid)
        listingrow.delete()
        try:
            w = Watchlist.objects.filter(user=request.user.username)
            wcount=len(w)
        except:
            wcount=None
        return render(request,"auctions/auctionwin.html",{
            "cb":cblist,
            "title":title,
            "wcount":wcount
        })   

    else:
        return redirect('index')


# This function makes a query to all the profits obtained    

def totalearnings(request):
    if request.user.username:
        articles=[]
        try:
            articleswin = Auctionclosed.objects.filter(winner=request.user.username)
            for w in articleswin:
                articles.append(Listtotal.objects.filter(listingid=w.listingid))
        except:
            articleswin = None
            articles = None
        try:
            w = Watchlist.objects.filter(user=request.user.username)
            wcount=len(w)
        except:
            wcount=None
        return render(request,'auctions/myauction.html',{
            "articles":articles,
            "wcount":wcount,
            "articleswin":articleswin
        })
    else:
        return redirect('index')

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
