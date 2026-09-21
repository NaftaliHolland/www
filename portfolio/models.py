from django.db import models

from modelcluster.fields import ParentalKey
from modelcluster.models import ClusterableModel
from wagtail.admin.panels import FieldPanel, InlinePanel, MultiFieldPanel
from wagtail.fields import RichTextField
from wagtail.models import Orderable, Page
from wagtail.snippets.models import register_snippet


@register_snippet
class ExperienceItem(ClusterableModel):
    role = models.CharField(max_length=255)
    organisation = models.CharField(max_length=255)
    date_range = models.CharField(max_length=100, help_text="e.g. 2024 — present")
    summary = models.TextField(blank=True)
    sort_order = models.PositiveIntegerField(
        default=0,
        help_text="Lower numbers show first (most recent role = 0).",
    )

    panels = [
        MultiFieldPanel(
            [
                FieldPanel("role"),
                FieldPanel("organisation"),
                FieldPanel("date_range"),
                FieldPanel("sort_order"),
                FieldPanel("summary"),
            ],
            heading="Role",
        ),
        InlinePanel("bullets", label="Highlights"),
    ]

    class Meta:
        ordering = ["sort_order"]

    def __str__(self):
        return f"{self.role} — {self.organisation}"


class ExperienceBullet(Orderable):
    item = ParentalKey(ExperienceItem, on_delete=models.CASCADE, related_name="bullets")
    text = models.CharField(max_length=255)

    panels = [FieldPanel("text")]

    def __str__(self):
        return self.text


class ProjectIndexPage(Page):
    intro = RichTextField(blank=True, features=["bold", "italic", "link"])

    subpage_types = ["portfolio.ProjectPage"]
    parent_page_types = ["home.HomePage"]

    content_panels = Page.content_panels + [FieldPanel("intro")]

    def get_context(self, request):
        context = super().get_context(request)
        context["projects"] = ProjectPage.objects.live().child_of(self).order_by("path")
        return context


class ProjectPage(Page):
    STATUS_CHOICES = [
        ("shipped", "Shipped"),
        ("in_progress", "In progress"),
        ("prototype", "Prototype"),
        ("concept", "Concept"),
    ]

    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default="concept")
    summary = models.TextField(help_text="One or two sentences shown on the project card.")
    body = RichTextField(blank=True, help_text="Optional longer write-up shown on the project's own page.")
    featured = models.BooleanField(
        default=False,
        help_text="Show this project in the 'Featured work' section on the homepage.",
    )
    link_url = models.URLField(blank=True, help_text="Optional link to a live demo or repo.")

    parent_page_types = ["portfolio.ProjectIndexPage"]
    subpage_types = []

    content_panels = Page.content_panels + [
        MultiFieldPanel(
            [
                FieldPanel("status"),
                FieldPanel("featured"),
                FieldPanel("link_url"),
            ],
            heading="Card settings",
        ),
        FieldPanel("summary"),
        FieldPanel("body"),
        InlinePanel("tech_tags", label="Tech stack tags"),
    ]

    @property
    def status_dot_class(self):
        return {
            "shipped": "bg-signal",
            "in_progress": "bg-amber",
            "prototype": "bg-muted",
            "concept": "bg-muted",
        }.get(self.status, "bg-muted")

    @property
    def status_text_class(self):
        return {
            "shipped": "text-signal",
            "in_progress": "text-amber",
            "prototype": "text-muted",
            "concept": "text-muted",
        }.get(self.status, "text-muted")


class ProjectTechTag(Orderable):
    page = ParentalKey(ProjectPage, on_delete=models.CASCADE, related_name="tech_tags")
    name = models.CharField(max_length=50)

    panels = [FieldPanel("name")]

    def __str__(self):
        return self.name


class TalkIndexPage(Page):
    intro = RichTextField(blank=True, features=["bold", "italic", "link"])
    empty_state_heading = models.CharField(
        max_length=255,
        default="I'm looking for my first talk.",
        help_text="Shown when there are no published talks yet.",
    )
    empty_state_body = models.TextField(
        blank=True,
        default="If you run a meetup, a lunch-and-learn, or a small conference and think one of the "
        "topics below would be a fit, I'd love to hear from you.",
    )

    subpage_types = ["portfolio.TalkPage"]
    parent_page_types = ["home.HomePage"]

    content_panels = Page.content_panels + [
        FieldPanel("intro"),
        MultiFieldPanel(
            [FieldPanel("empty_state_heading"), FieldPanel("empty_state_body")],
            heading="Empty state (shown while you have no talks yet)",
        ),
        InlinePanel("topics", label="Topics you could speak on"),
    ]

    def get_context(self, request):
        context = super().get_context(request)
        context["talks"] = TalkPage.objects.live().child_of(self).order_by("-date")
        return context


class TalkTopic(Orderable):
    page = ParentalKey(TalkIndexPage, on_delete=models.CASCADE, related_name="topics")
    title = models.CharField(max_length=255)
    description = models.TextField(blank=True)

    panels = [FieldPanel("title"), FieldPanel("description")]

    def __str__(self):
        return self.title


class TalkPage(Page):
    date = models.DateField(blank=True, null=True)
    venue = models.CharField(max_length=255, blank=True)
    description = RichTextField(blank=True, features=["bold", "italic", "link"])
    slides_url = models.URLField(blank=True)
    video_url = models.URLField(blank=True)

    parent_page_types = ["portfolio.TalkIndexPage"]
    subpage_types = []

    content_panels = Page.content_panels + [
        MultiFieldPanel(
            [FieldPanel("date"), FieldPanel("venue")],
            heading="Details",
        ),
        FieldPanel("description"),
        MultiFieldPanel(
            [FieldPanel("slides_url"), FieldPanel("video_url")],
            heading="Links",
        ),
    ]


class ArticleIndexPage(Page):
    intro = RichTextField(blank=True, features=["bold", "italic", "link"])

    subpage_types = ["portfolio.ArticlePage"]
    parent_page_types = ["home.HomePage"]

    content_panels = Page.content_panels + [FieldPanel("intro")]

    def get_context(self, request):
        context = super().get_context(request)
        context["articles"] = ArticlePage.objects.live().child_of(self).order_by("-first_published_at")
        return context


class ArticlePage(Page):
    STATUS_CHOICES = [
        ("published", "Published"),
        ("planned", "Planned"),
    ]

    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default="planned")
    summary = models.TextField(help_text="One or two sentences shown in the article list.")
    body = RichTextField(blank=True, help_text="Full article body. Leave blank while status is 'Planned'.")

    parent_page_types = ["portfolio.ArticleIndexPage"]
    subpage_types = []

    content_panels = Page.content_panels + [
        FieldPanel("status"),
        FieldPanel("summary"),
        FieldPanel("body"),
    ]


class ContactPage(Page):
    intro = models.TextField(
        blank=True,
        default="The best way to reach me is email — I read everything, even if I'm slow to reply "
        "some weeks.",
    )
    email = models.EmailField(blank=True)
    github_url = models.URLField(blank=True)
    linkedin_url = models.URLField(blank=True)
    location = models.CharField(max_length=255, blank=True, default="Kenya · open to remote")

    max_count = 1
    parent_page_types = ["home.HomePage"]
    subpage_types = []

    content_panels = Page.content_panels + [
        FieldPanel("intro"),
        MultiFieldPanel(
            [
                FieldPanel("email"),
                FieldPanel("github_url"),
                FieldPanel("linkedin_url"),
                FieldPanel("location"),
            ],
            heading="Contact details",
        ),
    ]
