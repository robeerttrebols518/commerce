from django.contrib import admin
from .models import User, Watchlist, Listing, Listtotal, Comment, Bid, Auctionclosed

# Register your models here.
admin.site.register(User)
admin.site.register(Watchlist)
admin.site.register(Listing)
admin.site.register(Listtotal)
admin.site.register(Comment)
admin.site.register(Bid)
admin.site.register(Auctionclosed)