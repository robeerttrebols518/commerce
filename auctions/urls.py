from django.urls import path

from . import views

urlpatterns = [
    path("", views.index, name="index"),
    path("login", views.login_view, name="login"),
    path("logout", views.logout_view, name="logout"),
    path("register", views.register, name="register"),
    path("createlist", views.createlist, name="createlist"),
    path("watchlist/<str:username>", views.pagelist, name="pagelist"),
    path("submit", views.submit, name="submit"),
    path("listings/<int:id>", views.pagelisttotal, name="pagelisttotal"),
    path("submitct/<int:listingid>", views.submitct, name="submitct"),
    path("uploadsubmit/<int:listingid>", views.uploadsubmit, name="uploadsubmit"),
    path("addtolist/<int:listingid>", views.addtolist, name="addtolist"),
    path("removelist/<int:listingid>", views.removelist, name="removelist"),
    path("categories", views.categories, name="categories"),
    path("category/<str:category>", views.category, name="category"),
    path("endauction/<int:listingid>", views.endauction, name="endauction"),
    path("totalearnings", views.totalearnings, name="totalearnings")
]
