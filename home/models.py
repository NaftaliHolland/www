from django.db import models
from modelcluster.fields import ParentalKey
from modelcluster.models import ClusterableModel
from wagtail.admin.panels import FieldPanel, MultiFieldPanel
from wagtail.fields import RichTextField
from wagtail.models import Orderable, Page
from wagtail.snippets.models import register_snippet


class HomePage(Page):
    image = models.ForeignKey(
        "wagtailimages.Image",
        null=True,
        blank=True,
        on_delete=models.SET_NULL,
        related_name="+"
    )
    hero_text = models.CharField(
        blank=True,
        max_length=255, help_text="Write an introduction for the site"
    )
    hero_cta = models.CharField(
        blank=True,
        verbose_name="Hero CTA",
        max_length=255,
        help_text="Text to display on call to Action",
    )
    hero_cta_link = models.ForeignKey(
        "wagtailcore.Page",
        null=True,
        blank=True,
        on_delete=models.SET_NULL,
        related_name="+",
        verbose_name="Hero CTA link",
        help_text="Choose a page to link to the call to Action",
    )
    body = RichTextField(blank=True)

    content_panels = Page.content_panels + [
        MultiFieldPanel(
            [
                FieldPanel("image"),
                FieldPanel("hero_text"),
                FieldPanel("hero_cta"),
                FieldPanel("hero_cta_link"),
            ],
            heading="Hero section"
        ),
        FieldPanel('body'),
    ]


@register_snippet
class HomePageAside(ClusterableModel):
    name = models.CharField(max_length=255)
    role = models.CharField(max_length=255, blank=True, null=True)
    
    panels = ["name", "role", "nav_links", "social_links"]

    class Meta:
        verbose_name_plural = "Home Page Aside"

class HomePageNavLinks(Orderable):
    parent = ParentalKey(
        HomePageAside,
        related_name="nav_links",
        on_delete=models.CASCADE,
    )
    title = models.CharField(max_length=20)
    anchor = models.CharField(
        max_length=50,
        help_text="Section ID"
    )
    panels = [
        FieldPanel("title"),
        FieldPanel("anchor"),
    ]

class HomePageSocialLinks(Orderable):
    parent = ParentalKey(
        HomePageAside,
        related_name="social_links",
        on_delete=models.CASCADE,
    )
    title = models.CharField(max_length=20)
    url = models.URLField(
        max_length=255,
        help_text="Link to social profile",
        blank=True,
        null=True,
    )
    panels = [
        FieldPanel("title"),
        FieldPanel("url"),
    ]
