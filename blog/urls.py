
from django.urls import path
from . import views

app_name = 'blog'

urlpatterns = [
    path("", views.home, name="home"),
    path("about/", views.about, name="about"),
    path("mosque/", views.mosque, name="mosque"),
    path("blog/", views.blog, name="blog"),
    path("blog/<str:slug>/", views.blog_single, name="blog_single"),
    path("search/", views.search, name="search"),
    path("courses/", views.courses, name="courses"),
    path("project/<str:slug>/", views.singleproject, name="project_single"),
    path("course/<str:slug>/", views.course_single, name="course_single"),
    path("contact/", views.contact, name="contact"),
    path("not/", views.not_found, name="not_found"),
]