from django import template
import jdatetime

register = template.Library()


@register.filter
def jdate(value, fmt="%Y/%m/%d"):
    """تبدیل تاریخ میلادی به شمسی"""
    if not value:
        return ""
    
    try:
        # اگه datetime بود
        if hasattr(value, 'date'):
            value = value.date()
        
        # تبدیل میلادی به شمسی
        jd = jdatetime.date.fromgregorian(date=value)
        
        # تبدیل فرمت‌های ساده به پایتونی
        fmt = fmt.replace("j", "%d").replace("F", "%B").replace("Y", "%Y")
        
        return jd.strftime(fmt)
    except Exception as e:
        return value