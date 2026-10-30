from django.shortcuts import render, get_object_or_404, redirect
from django.contrib import messages
from .forms import ContactForm,TestimonialForm
from django.core.paginator import Paginator
from .models import BlogPost, Category, Tag, Comment, Project, ContactMessage,Course,CourseCategory,Testimonial,TeamMember,Occasion,DailyMotivation
from django.http import HttpResponseNotFound
from django.db.models import Q

import jdatetime
import random


def home(request):
    """صفحه اصلی"""
    latest_posts = BlogPost.objects.filter(is_published=True)[:6]
    latest_articles = BlogPost.objects.filter(is_published=True)[:4]
    featured_posts = BlogPost.objects.filter(is_published=True, is_featured=True)[:3]
    featured_projects = Project.objects.filter(is_published=True, is_featured=True)[:3]
    team_members = TeamMember.objects.filter(is_active=True)
    
    # ✅ اصلاح شد: فقط نظرات تأییدشده
    testimonials = Testimonial.objects.filter(is_active=True, is_approved=True)[:10]
    categories = Category.objects.all()

    if not featured_projects:
        featured_projects = Project.objects.filter(is_published=True)[:3]

    # ---- مناسبت امروز یا پیام انگیزشی ----
    # ---- مناسبت امروز یا پیام انگیزشی ----
    today = jdatetime.date.today()
    today_str = f"{today.month:02d}/{today.day:02d}"

    # روزهای هفته به فارسی
    weekdays = ['شنبه', 'یک‌شنبه', 'دوشنبه', 'سه‌شنبه', 'چهارشنبه', 'پنج‌شنبه', 'جمعه']
    weekday = weekdays[today.weekday()]

    # ماه‌های شمسی
    months = ['فروردین', 'اردیبهشت', 'خرداد', 'تیر', 'مرداد', 'شهریور',
              'مهر', 'آبان', 'آذر', 'دی', 'بهمن', 'اسفند']
    month_name = months[today.month - 1]

    today_jalali = f"{today.day} {month_name}"   # مثلاً: ۲۸ تیر

    occasion = Occasion.objects.filter(
        jalali_date=today_str, is_active=True
    ).first()

    motivation = None
    if not occasion:
        motivations = list(DailyMotivation.objects.filter(is_active=True))
        if motivations:
            motivation = random.choice(motivations)

    context = {
        'latest_posts': latest_posts,
        'latest_articles': latest_articles,
        'featured_posts': featured_posts,
        'featured_projects': featured_projects,
        'team_members': team_members,
        'testimonials': testimonials,
        'categories': categories,
        'occasion': occasion,       # ← جدید
        'motivation': motivation,   # ← جدید
        'today_jalali': today_jalali,   # ← جدید

    }
    return render(request, 'blog/index.html', context)



def search(request):
    """جستجو در مطالب، پروژه‌ها و دوره‌ها"""
    query = request.GET.get('q', '').strip()

    posts = []
    projects = []
    courses = []

    if query:
        posts = BlogPost.objects.filter(
            Q(title__icontains=query) |
            Q(short_description__icontains=query) |
            Q(content__icontains=query),
            is_published=True
        )
        projects = Project.objects.filter(
            Q(title__icontains=query) |
            Q(short_description__icontains=query) |
            Q(description__icontains=query),
            is_published=True
        )
        courses = Course.objects.filter(
            Q(title__icontains=query) |
            Q(short_description__icontains=query) |
            Q(description__icontains=query),
            is_published=True
        )

    # اگه هیچی پیدا نشد → برو به ۴۰۴
    if query and not posts and not projects and not courses:
        return render(request, 'blog/404.html', {'query': query}, status=404)

    context = {
        'query': query,
        'posts': posts,
        'projects': projects,
        'courses': courses,
    }
    return render(request, 'blog/search.html', context)


def about(request):
    if request.method == 'POST':
        form = TestimonialForm(request.POST, request.FILES)
        if form.is_valid():
            testimonial = form.save(commit=False)
            testimonial.is_approved = False
            testimonial.save()
            messages.success(
                request,
                'نظر شما با موفقیت ثبت شد. پس از تأیید ادمین در سایت نمایش داده می‌شود. 🌸'
            )
            return redirect('blog:about')
        else:
            messages.error(request, 'لطفاً خطاهای فرم را برطرف کنید.')
    else:
        form = TestimonialForm()

    context = {
        'form': form,
        'team_members': TeamMember.objects.filter(is_active=True),  # ← اگه داری
    }
    return render(request, 'blog/about.html', context)


def mosque(request):
    """صفحه درباره ما"""
    team_members = TeamMember.objects.filter(is_active=True)
    testimonials = Testimonial.objects.filter(is_active=True)
    
    context = {
        'team_members': team_members,
        'testimonials': testimonials,
    }
    return render(request, 'blog/mosque.html', context)


def blog(request):
    """لیست مطالب وبلاگ"""
    posts_list = BlogPost.objects.filter(is_published=True)
    paginator = Paginator(posts_list, 6)
    page_number = request.GET.get('page')
    posts = paginator.get_page(page_number)

    categories = Category.objects.all()
    tags = Tag.objects.all()

    context = {
        'posts': posts,
        'categories': categories,
        'tags': tags,
    }
    return render(request, 'blog/blog.html', context)



def blog_single(request, slug):
    """جزئیات مطلب"""
    post = get_object_or_404(BlogPost, slug=slug, is_published=True)

    if request.method == 'POST':
        name = request.POST.get('name')
        email = request.POST.get('email')
        message = request.POST.get('message')
        parent_id = request.POST.get('parent_id')   # ← جدید

        if name and email and message:
            parent = None
            if parent_id:
                try:
                    parent = Comment.objects.get(id=parent_id, post=post)
                except Comment.DoesNotExist:
                    parent = None

            Comment.objects.create(
                post=post,
                parent=parent,                       # ← جدید
                name=name,
                email=email,
                message=message,
                is_approved=False,
            )
            messages.success(request, 'نظر شما ثبت شد. پس از تأیید مدیر نمایش داده می‌شود.')
            return redirect('blog:blog_single', slug=post.slug)

    post.view_count += 1
    post.save()

    comments = post.comments.filter(is_approved=True, parent=None)
    related_posts = BlogPost.objects.filter(
        category=post.category, is_published=True
    ).exclude(id=post.id)[:2]

    context = {
        'post': post,
        'comments': comments,
        'related_posts': related_posts,
    }
    return render(request, 'blog/blog-single.html', context)


def courses(request):
    """لیست دوره‌های آشیانه جوان"""
    courses_list = Course.objects.filter(is_published=True)

    # فیلتر بر اساس دسته
    category_slug = request.GET.get('category')
    current_category = None
    if category_slug:
        current_category = get_object_or_404(CourseCategory, slug=category_slug)
        courses_list = courses_list.filter(category=current_category)

    # صفحه‌بندی
    paginator = Paginator(courses_list, 9)
    page_number = request.GET.get('page')
    courses = paginator.get_page(page_number)

    # همه دسته‌بندی‌ها
    categories = CourseCategory.objects.all()

    context = {
        'courses': courses,
        'categories': categories,
        'current_category': current_category,
    }
    return render(request, 'blog/courses.html', context)

def singleproject(request, slug):
    """جزئیات پروژه"""
    project = get_object_or_404(Project, slug=slug, is_published=True)
    related_projects = Project.objects.filter(
        category=project.category, is_published=True
    ).exclude(id=project.id)[:3]

    context = {
        'project': project,
        'related_projects': related_projects,
    }
    return render(request, 'blog/project-single.html', context)


def course_single(request, slug):
    """جزئیات دوره"""
    course = get_object_or_404(Course, slug=slug, is_published=True)
    related_courses = Course.objects.filter(is_published=True).exclude(id=course.id)[:3]

    context = {
        'course': course,
        'related_courses': related_courses,
    }
    return render(request, 'blog/course-single.html', context)

def contact(request):
    """صفحه تماس با ما"""
    if request.method == 'POST':
        form = ContactForm(request.POST)
        if form.is_valid():
            ContactMessage.objects.create(
                name=form.cleaned_data['name'],
                email=form.cleaned_data['email'],
                subject=form.cleaned_data.get('subject', ''),
                phone=form.cleaned_data.get('phone', ''),
                message=form.cleaned_data['message'],
            )
            messages.success(request, 'پیام شما با موفقیت ارسال شد. به‌زودی با شما تماس می‌گیریم.')
            return redirect('blog:contact')
    else:
        form = ContactForm()

    return render(request, 'blog/contact.html', {'form': form})


def not_found(request, exception=None):
    """صفحه ۴۰۴ سفارشی"""
    return HttpResponseNotFound(
        render(request, 'blog/404.html').content
    )