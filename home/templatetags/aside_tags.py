from django import template

from home.models import HomePageAside

register = template.Library()

@register.inclusion_tag('home/includes/home_aside.html', takes_context=True)
def aside(context):
    # I really don't like this, TODO: Find a better way to have a 'singleton'
    home_page_aside = HomePageAside.objects.all().first()
    return {
        "name": home_page_aside.name,
        "role": home_page_aside.role,
        "nav_links": home_page_aside.nav_links,
        "social_links": home_page_aside.social_links,
    }
