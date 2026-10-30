from django import forms
# بعداً پر می‌شه
from django import forms
from django.core.validators import RegexValidator
from .models import Testimonial


class TestimonialForm(forms.ModelForm):
    class Meta:
        model = Testimonial
        fields = ['name', 'role', 'title', 'message', 'image']
        widgets = {
            'name': forms.TextInput(attrs={
                'class': 'w-full border border-gray rounded-md p-3 focus:outline-none focus:ring-0 focus:border-primary',
                'placeholder': 'نام و نام خانوادگی',
            }),
            'role': forms.TextInput(attrs={
                'class': 'w-full border border-gray rounded-md p-3 focus:outline-none focus:ring-0 focus:border-primary',
                'placeholder': 'مثلاً: طلبه پایه ۳',
            }),
            'title': forms.TextInput(attrs={
                'class': 'w-full border border-gray rounded-md p-3 focus:outline-none focus:ring-0 focus:border-primary',
                'placeholder': 'یک جمله کوتاه (اختیاری)',
            }),
            'message': forms.Textarea(attrs={
                'class': 'w-full border border-gray rounded-md p-3 focus:outline-none focus:ring-0 focus:border-primary',
                'rows': 4,
                'placeholder': 'تجربه‌ی خود را بنویسید...',
            }),
            'image': forms.ClearableFileInput(attrs={
                'class': 'w-full border border-gray rounded-md p-3 focus:outline-none focus:ring-0 focus:border-primary',
            }),
        }
        labels = {
            'name': 'نام و نام خانوادگی',
            'role': 'سمت / عنوان',
            'title': 'عنوان (اختیاری)',
            'message': 'متن تجربه',
            'image': 'تصویر (اختیاری)',
        }

class ContactForm(forms.Form):
    """فرم تماس با ما"""
    name = forms.CharField(
        max_length=100,
        label="نام",
        error_messages={
            'required': 'لطفاً نام خود را وارد کنید.',
            'max_length': 'نام نمی‌تواند بیش از ۱۰۰ کاراکتر باشد.',
        },
        widget=forms.TextInput(attrs={
            'class': 'from-control',
            'placeholder': 'نام*',
        })
    )
    email = forms.EmailField(
        label="ایمیل",
        error_messages={
            'required': 'لطفاً ایمیل خود را وارد کنید.',
            'invalid': 'ایمیل وارد شده معتبر نیست.',
        },
        widget=forms.EmailInput(attrs={
            'class': 'from-control',
            'placeholder': 'ایمیل*',
        })
    )
    subject = forms.CharField(
        max_length=200,
        required=False,
        label="موضوع",
        error_messages={
            'max_length': 'موضوع نمی‌تواند بیش از ۲۰۰ کاراکتر باشد.',
        },
        widget=forms.TextInput(attrs={
            'class': 'from-control',
            'placeholder': 'موضوع',
        })
    )
    phone = forms.CharField(
    max_length=20,
    label="شماره تماس",
    validators=[
        RegexValidator(
            regex=r'^[0-9۰-۹+\-\s]+$',
            message='شماره تماس فقط می‌تواند شامل عدد، + و - باشد.',
        )
    ],
    error_messages={
        'required': 'لطفاً شماره تماس خود را وارد کنید.',
    },
    widget=forms.TextInput(attrs={
        'class': 'from-control',
        'placeholder': 'شماره تماس*',
    })
)
    message = forms.CharField(
        label="پیام",
        error_messages={
            'required': 'لطفاً متن پیام خود را وارد کنید.',
        },
        widget=forms.Textarea(attrs={
            'class': 'from-control',
            'placeholder': 'پیام شما*',
            'rows': 5,
        })
    )