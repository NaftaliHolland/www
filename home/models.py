from django.db import models
from modelcluster.fields import ParentalKey
from modelcluster.models import ClusterableModel
from portfolio.blocks import PortfolioStreamBlock
from wagtail.admin.panels import FieldPanel, MultiFieldPanel
from wagtail.blocks import CharBlock, RichTextBlock, StructBlock
from wagtail.fields import RichTextField, StreamField
from wagtail.models import Orderable, Page
from wagtail.snippets.models import register_snippet


class HomePage(Page):
    about = RichTextField(features=["bold", "italic", "link"])
    projects = StreamField(
        PortfolioStreamBlock(),
        blank=True,
        use_json_field=True,
        help_text="Use this section to list your projects.",
    )
    experience = StreamField([
        ('experience', StructBlock([
            ('company', CharBlock(required=False)),
            ('role', CharBlock(required=False)),
            ('period', CharBlock()),
            ('description', RichTextBlock(features=["bold", "italic", "link"])),
            ('tags', CharBlock(required=False, help_text="Enter comma-separated tags")),
        ]))
    ])

    content_panels = Page.content_panels + [
        "about",
        "experience",
        FieldPanel("projects"),
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
