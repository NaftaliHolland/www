from wagtail.admin.panels import FieldPanel
from wagtail.fields import StreamField
from wagtail.models import Page

from portfolio.blocks import PortfolioStreamBlock


class PortfolioPage(Page):
    parent_page_type = ["home.HomePage"]

    body = StreamField(
        PortfolioStreamBlock(),
        blank=True,
        use_json_field=True,
        help_text="Use this section to list your projects and skills.",
    )

    content_panels = Page.content_panels + [
        FieldPanel("body"),
    ]
