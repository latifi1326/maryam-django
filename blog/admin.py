from django.contrib import admin
from .models import Category, Tag, BlogPost, Comment, Project, ContactMessage,CourseCategory,Course,TeamMember,Testimonial,DailyMotivation,Occasion

# Register your models here.

@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ('name', 'slug', 'created_at')
    search_fields = ('name',)
    prepopulated_fields = {'slug': ('name',)}
    readonly_fields = ('created_at',)


@admin.register(Tag)
class TagAdmin(admin.ModelAdmin):
    list_display = ('name', 'slug')
    search_fields = ('name',)
    prepopulated_fields = {'slug': ('name',)}


@admin.register(BlogPost)
class BlogPostAdmin(admin.ModelAdmin):
    list_display = ('title', 'category', 'author', 'is_published', 'is_featured', 'created_at')
    list_filter = ('is_published', 'is_featured', 'category')
    search_fields = ('title', 'short_description', 'content')
    prepopulated_fields = {'slug': ('title',)}
    readonly_fields = ('view_count', 'created_at', 'updated_at')
    filter_horizontal = ('tags',)
    list_editable = ('is_published', 'is_featured')


@admin.register(Comment)
class CommentAdmin(admin.ModelAdmin):
    list_display = ('name', 'email', 'post', 'short_message', 'is_approved', 'created_at')
    list_filter = ('is_approved', 'created_at')
    search_fields = ('name', 'email', 'message')
    list_editable = ('is_approved',)
    readonly_fields = ('created_at', 'short_message')

    def short_message(self, obj):
        """نمایش خلاصه پیام (۵۰ کاراکتر اول)"""
        if obj.message:
            return obj.message[:50] + ('...' if len(obj.message) > 50 else '')
        return '-'
    short_message.short_description = "متن پیام"


@admin.register(Project)
class ProjectAdmin(admin.ModelAdmin):
    list_display = ('title', 'category', 'location', 'event_date', 'is_published', 'is_featured')
    list_filter = ('is_published', 'is_featured', 'category', 'event_date')
    search_fields = ('title', 'short_description', 'description', 'location')
    prepopulated_fields = {'slug': ('title',)}
    readonly_fields = ('created_at',)
    list_editable = ('is_published', 'is_featured')


@admin.register(ContactMessage)
class ContactMessageAdmin(admin.ModelAdmin):
    list_display = ('name', 'email', 'subject', 'phone', 'is_read', 'created_at')
    list_filter = ('is_read', 'created_at')
    search_fields = ('name', 'email', 'subject', 'phone', 'message')
    list_editable = ('is_read',)
    readonly_fields = ('name', 'email', 'subject', 'phone', 'message', 'created_at')

@admin.register(CourseCategory)
class CourseCategoryAdmin(admin.ModelAdmin):
    list_display = ('name', 'slug', 'created_at')
    search_fields = ('name',)
    prepopulated_fields = {'slug': ('name',)}
    readonly_fields = ('created_at',)


@admin.register(Course)
class CourseAdmin(admin.ModelAdmin):
    list_display = ('title', 'category', 'instructor', 'level', 'is_published', 'is_featured')
    list_filter = ('is_published', 'is_featured', 'level', 'category')
    search_fields = ('title', 'short_description', 'description', 'instructor')
    prepopulated_fields = {'slug': ('title',)}
    readonly_fields = ('created_at',)
    list_editable = ('is_published', 'is_featured')

@admin.register(TeamMember)
class TeamMemberAdmin(admin.ModelAdmin):
    list_display = ('name', 'position', 'order', 'is_active')
    list_filter = ('is_active',)
    search_fields = ('name', 'position')
    list_editable = ('order', 'is_active')




@admin.register(Testimonial)
class TestimonialAdmin(admin.ModelAdmin):
    list_display = ('name', 'role', 'title', 'is_approved', 'is_active', 'created_at')
    list_filter = ('is_approved', 'is_active', 'created_at')
    search_fields = ('name', 'role', 'title', 'message')
    list_editable = ('is_approved', 'is_active')
    ordering = ('-created_at',)


@admin.register(Occasion)
class OccasionAdmin(admin.ModelAdmin):
    list_display = ('title', 'jalali_date','footer_text', 'is_active')
    list_filter = ('is_active',)
    search_fields = ('title', 'description', 'footer_text','jalali_date',)
    list_editable = ('is_active',)


@admin.register(DailyMotivation)
class DailyMotivationAdmin(admin.ModelAdmin):
    list_display = ('__str__', 'footer_text','is_active')
    list_filter = ('is_active',)
    list_editable = ('is_active',)