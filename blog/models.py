from django.db import models
from django.utils.text import slugify

#creat yout models here
class Category(models.Model):
    """دسته‌بندی مطالب"""
    name = models.CharField(max_length=100, verbose_name="نام دسته")
    slug = models.SlugField(unique=True, verbose_name="اسلاگ", allow_unicode=True)
    created_at = models.DateTimeField(auto_now_add=True, verbose_name="تاریخ ایجاد")

    class Meta:
        verbose_name = "دسته‌بندی"
        verbose_name_plural = "دسته‌بندی‌ها"
        ordering = ['name']

    def __str__(self):
        return self.name

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.name, allow_unicode=True)
        super().save(*args, **kwargs)


class Tag(models.Model):
    """برچسب‌های مطالب"""
    name = models.CharField(max_length=50, unique=True, verbose_name="نام برچسب")
    slug = models.SlugField(unique=True, verbose_name="اسلاگ", allow_unicode=True)

    class Meta:
        verbose_name = "برچسب"
        verbose_name_plural = "برچسب‌ها"
        ordering = ['name']

    def __str__(self):
        return self.name

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.name, allow_unicode=True)
        super().save(*args, **kwargs)


class BlogPost(models.Model):
    """مطالب وبلاگ"""
    title = models.CharField(max_length=200, verbose_name="عنوان")
    slug = models.SlugField(unique=True, verbose_name="اسلاگ", allow_unicode=True)
    category = models.ForeignKey(
        Category,
        on_delete=models.CASCADE,
        related_name='posts',
        verbose_name="دسته‌بندی"
    )
    tags = models.ManyToManyField(
        Tag,
        blank=True,
        related_name='posts',
        verbose_name="برچسب‌ها"
    )
    author = models.CharField(max_length=100, default="مدیر", verbose_name="نویسنده")
    image = models.ImageField(upload_to='blog/', verbose_name="تصویر شاخص")
    short_description = models.TextField(max_length=300, verbose_name="توضیح کوتاه")
    content = models.TextField(verbose_name="محتوا")
    is_published = models.BooleanField(default=True, verbose_name="منتشر شده")
    is_featured = models.BooleanField(default=False, verbose_name="مطلب ویژه")
    view_count = models.PositiveIntegerField(default=0, verbose_name="تعداد بازدید")
    created_at = models.DateTimeField(auto_now_add=True, verbose_name="تاریخ ایجاد")
    updated_at = models.DateTimeField(auto_now=True, verbose_name="آخرین ویرایش")

    class Meta:
        verbose_name = "مطلب وبلاگ"
        verbose_name_plural = "مطالب وبلاگ"
        ordering = ['-created_at']

    def __str__(self):
        return self.title

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.title, allow_unicode=True)
        super().save(*args, **kwargs)


class Comment(models.Model):
    """نظرات مطالب"""
    post = models.ForeignKey(
        BlogPost,
        on_delete=models.CASCADE,
        related_name='comments',
        verbose_name="مطلب"
    )
    parent = models.ForeignKey(
        'self',
        on_delete=models.CASCADE,
        null=True,
        blank=True,
        related_name='replies',
        verbose_name="پاسخ به"
    )
    name = models.CharField(max_length=100, verbose_name="نام")
    email = models.EmailField(verbose_name="ایمیل")
    website = models.URLField(blank=True, null=True, verbose_name="وبسایت")
    message = models.TextField(verbose_name="پیام")
    is_approved = models.BooleanField(default=False, verbose_name="تأیید شده")
    created_at = models.DateTimeField(auto_now_add=True, verbose_name="تاریخ ایجاد")

    class Meta:
        verbose_name = "نظر"
        verbose_name_plural = "نظرات"
        ordering = ['-created_at']

    def __str__(self):
        return f"{self.name} - {self.post.title[:30]}"


class Project(models.Model):
    """پروژه‌ها و برنامه‌های مدرسه (آشیانه جوان)"""
    title = models.CharField(max_length=200, verbose_name="عنوان")
    slug = models.SlugField(unique=True, verbose_name="اسلاگ", allow_unicode=True)
    category = models.ForeignKey(
        Category,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='projects',
        verbose_name="دسته‌بندی"
    )
    image = models.ImageField(upload_to='projects/', verbose_name="تصویر")
    short_description = models.TextField(max_length=300, verbose_name="توضیح کوتاه")
    description = models.TextField(verbose_name="توضیحات کامل")
    location = models.CharField(max_length=200, blank=True, null=True, verbose_name="مکان")
    event_date = models.DateField(blank=True, null=True, verbose_name="تاریخ برگزاری")
    is_published = models.BooleanField(default=True, verbose_name="منتشر شده")
    is_featured = models.BooleanField(default=False, verbose_name="ویژه")
    created_at = models.DateTimeField(auto_now_add=True, verbose_name="تاریخ ایجاد")

    class Meta:
        verbose_name = "مناسبت"
        verbose_name_plural = "مناسبت ها"
        ordering = ['-created_at']

    def __str__(self):
        return self.title

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.title, allow_unicode=True)
        super().save(*args, **kwargs)


class ContactMessage(models.Model):
    """پیام‌های فرم تماس"""
    name = models.CharField(max_length=100, verbose_name="نام")
    email = models.EmailField(verbose_name="ایمیل")
    subject = models.CharField(max_length=200, blank=True, null=True, verbose_name="موضوع")
    phone = models.CharField(max_length=20, blank=True, null=True, verbose_name="شماره تماس")
    message = models.TextField(verbose_name="پیام")
    is_read = models.BooleanField(default=False, verbose_name="خوانده شده")
    created_at = models.DateTimeField(auto_now_add=True, verbose_name="تاریخ ارسال")

    class Meta:
        verbose_name = "پیام تماس"
        verbose_name_plural = "پیام‌های تماس"
        ordering = ['-created_at']

    def __str__(self):
        return f"{self.name} - {self.subject or 'بدون موضوع'}"
    
class CourseCategory(models.Model):
    """دسته‌بندی دوره‌های آشیانه جوان"""
    name = models.CharField(max_length=100, verbose_name="نام دسته")
    slug = models.SlugField(unique=True, verbose_name="اسلاگ", allow_unicode=True)
    description = models.TextField(blank=True, null=True, verbose_name="توضیحات")
    created_at = models.DateTimeField(auto_now_add=True, verbose_name="تاریخ ایجاد")

    class Meta:
        verbose_name = "دسته دوره"
        verbose_name_plural = "دسته‌های دوره"
        ordering = ['name']

    def __str__(self):
        return self.name

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.name, allow_unicode=True)
        super().save(*args, **kwargs)
        
class Course(models.Model):
    """دوره‌های آموزشی بنیاد آشیانه جوان"""
    title = models.CharField(max_length=200, verbose_name="عنوان دوره")
    slug = models.SlugField(unique=True, verbose_name="اسلاگ", allow_unicode=True)
    category = models.ForeignKey(   # ← این فیلد اضافه شد
        CourseCategory,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='courses',
        verbose_name="دسته‌بندی"
    )
    image = models.ImageField(upload_to='courses/', verbose_name="تصویر دوره")
    short_description = models.TextField(max_length=300, verbose_name="توضیح کوتاه")
    description = models.TextField(verbose_name="توضیحات کامل")
    instructor = models.CharField(max_length=200, blank=True, null=True, verbose_name="مدرس")
    level = models.CharField(max_length=100, blank=True, null=True, verbose_name="سطح (مقدماتی/پیشرفته)")
    duration = models.CharField(max_length=100, blank=True, null=True, verbose_name="مدت دوره")
    schedule = models.CharField(max_length=200, blank=True, null=True, verbose_name="زمان‌بندی")
    is_published = models.BooleanField(default=True, verbose_name="منتشر شده")
    is_featured = models.BooleanField(default=False, verbose_name="ویژه")
    created_at = models.DateTimeField(auto_now_add=True, verbose_name="تاریخ ایجاد")

    class Meta:
        verbose_name = "دوره"
        verbose_name_plural = "دوره‌ها"
        ordering = ['-created_at']

    def __str__(self):
        return self.title

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.title, allow_unicode=True)
        super().save(*args, **kwargs)

class TeamMember(models.Model):
    """اعضای کادر علمی و آموزشی"""
    name = models.CharField(max_length=100, verbose_name="نام")
    position = models.CharField(max_length=150, verbose_name="سمت")
    image = models.ImageField(upload_to='team/', verbose_name="تصویر")
    facebook = models.URLField(blank=True, null=True, verbose_name="فیسبوک")
    twitter = models.URLField(blank=True, null=True, verbose_name="توییتر")
    linkedin = models.URLField(blank=True, null=True, verbose_name="لینکدین")
    order = models.PositiveIntegerField(default=0, verbose_name="ترتیب نمایش")
    is_active = models.BooleanField(default=True, verbose_name="فعال")
    created_at = models.DateTimeField(auto_now_add=True, verbose_name="تاریخ ایجاد")

    class Meta:
        verbose_name = "عضو تیم"
        verbose_name_plural = "اعضای تیم"
        ordering = ['order', 'name']

    def __str__(self):
        return f"{self.name} - {self.position}"
    
class Testimonial(models.Model):
    """نظرات طلاب و دانش‌آموختگان"""
    name = models.CharField(max_length=100, verbose_name="نام")
    role = models.CharField(max_length=150, verbose_name="سمت/عنوان")
    title = models.CharField(max_length=200, verbose_name="عنوان نظر (یک جمله کوتاه)", blank=True)
    message = models.TextField(verbose_name="متن نظر")
    image = models.ImageField(upload_to='testimonials/', blank=True, null=True, verbose_name="تصویر (اختیاری)")
    order = models.PositiveIntegerField(default=0, verbose_name="ترتیب نمایش")
    is_active = models.BooleanField(default=True, verbose_name="فعال")
    created_at = models.DateTimeField(auto_now_add=True, verbose_name="تاریخ ایجاد")
    email = models.EmailField(blank=True, null=True, verbose_name="ایمیل (اختیاری)")
    is_approved = models.BooleanField(default=False, verbose_name="تأیید شده توسط ادمین")

    class Meta:
        verbose_name = "نظر طلبه"
        verbose_name_plural = "نظرات طلاب"
        ordering = ['order', '-created_at']

    def __str__(self):
        return f"{self.name} - {self.role}"
    
class Occasion(models.Model):
    """مناسبت‌های روزانه (تقویم شمسی)"""
    title = models.CharField(max_length=200, verbose_name="عنوان مناسبت")
    description = models.TextField(verbose_name="توضیحات")
    footer_text = models.CharField(
        max_length=200,
        blank=True,
        default="مدرسه علمیه حضرت مریم (س)",
        verbose_name="متن امضا (اختیاری)"
    )
    image = models.ImageField(upload_to='occasions/', blank=True, null=True, verbose_name="تصویر")
    jalali_date = models.CharField(
        max_length=5,
        verbose_name="تاریخ شمسی (ماه/روز)",
        help_text="فرمت: MM/DD — مثال: 07/03 برای ۳ مهر",
        unique=True
    )
    
    is_active = models.BooleanField(default=True, verbose_name="فعال")

    class Meta:
        verbose_name = "حدیث مناسبتی"
        verbose_name_plural = "حدیث های مناسبتی"
        ordering = ['jalali_date']

    def __str__(self):
        return f"{self.jalali_date} - {self.title}"


class DailyMotivation(models.Model):
    """آیه  برای روزهای بدون مناسبت"""
    text = models.TextField(verbose_name="متن انگیزشی")
    footer_text = models.CharField(
        max_length=200,
        blank=True,
        default="مدرسه علمیه حضرت مریم (س)",
        verbose_name="متن امضا (اختیاری)"
    )
    image = models.ImageField(upload_to='motivations/', blank=True, null=True, verbose_name="تصویر")
    is_active = models.BooleanField(default=True, verbose_name="فعال")

    class Meta:
        verbose_name = "حدیث روز"
        verbose_name_plural = "حدیث های روز "

    def __str__(self):
        return self.text[:50]