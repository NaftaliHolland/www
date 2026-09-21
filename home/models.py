from django.db import models

from modelcluster.fields import ParentalKey
from wagtail.admin.panels import FieldPanel, InlinePanel, MultiFieldPanel
from wagtail.fields import RichTextField
from wagtail.models import Orderable, Page


class HomePage(Page):
    max_count = 1

    home_subtitle = models.CharField(
        max_length=60,
        default="holland@dev:~$ whoami",
        help_text="Small mono eyebrow line above the headline.",
    )
    hero_heading = models.CharField(
        max_length=255,
        default="I build systems that work — then I make sure they work for the people who actually use them.",
    )
    about_text = RichTextField(
        blank=True,
        features=["bold", "italic", "link"],
        help_text="One or more paragraphs introducing you. Rendered under the hero heading.",
    )

    contact_heading = models.CharField(max_length=255, default="Let's build something.")
    contact_body = models.TextField(
        blank=True,
        default="Open to conversations about engineering roles, collaboration, or anything backend-and-Africa shaped.",
    )

    content_panels = Page.content_panels + [
        MultiFieldPanel(
            [
                FieldPanel("home_subtitle"),
                FieldPanel("hero_heading"),
                FieldPanel("about_text"),
            ],
            heading="Hero & about",
        ),
        InlinePanel("skills", label="Skill tags", help_text="Short tags shown under the about text, e.g. React, Go."),
        MultiFieldPanel(
            [
                FieldPanel("contact_heading"),
                FieldPanel("contact_body"),
            ],
            heading="Contact call-to-action",
        ),
    ]

    def get_context(self, request):
        context = super().get_context(request)

        from portfolio.models import ArticlePage, ExperienceItem, ProjectPage, TalkPage

        context["experience_items"] = ExperienceItem.objects.all().prefetch_related("bullets")
        context["featured_projects"] = (
            ProjectPage.objects.live().filter(featured=True).order_by("path")[:4]
        )
        context["latest_talks"] = TalkPage.objects.live().order_by("-date")[:1]
        context["latest_articles"] = ArticlePage.objects.live().order_by("-first_published_at")[:3]
        return context

    class Meta:
        verbose_name = "Homepage"


class HomePageSkill(Orderable):
    page = ParentalKey(HomePage, on_delete=models.CASCADE, related_name="skills")
    name = models.CharField(max_length=50)

    panels = [FieldPanel("name")]

    def __str__(self):
        return self.name
