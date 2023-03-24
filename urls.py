from django.urls import path,include

from . import views

urlpatterns = [
    path('',views.index,name="index"),
    path('loginform/',views.loginform,name="loginform"),
    path('login/',views.login,name="login"),
    path('registerform/',views.registerform,name="registerform"),
    path('register/',views.register,name="register"),
    path('logout/',views.logout,name="logout"),
    path('trainform/',views.trainform,name="trainform"),
    path('addtrain/',views.addtrain,name="addtrains"),
    path('<train_id>',views.train_id,name="train_id"),
    path('book/',views.book,name="book"),
    path('bookform/',views.bookform,name="bookform"),
    path('mybooking/',views.mybooking,name="mybooking"),
    path('booking/<train_id>',views.booking,name="booking"),
    path('pay/<int:r_id>',views.pay,name="pay"),
    path('delete/<int:r_id>',views.delete,name="delete"),
    path('payupdate/<int:r_id>',views.payupdate,name="payupdate"),
    path('get_ticket/<int:r_id>',views.get_ticket,name="get_ticket")
]
