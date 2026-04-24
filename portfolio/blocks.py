from base.blocks import BaseStreamBlock
from wagtail.blocks import (CharBlock, ListBlock, PageChooserBlock,
                            RichTextBlock, StructBlock, StructValue)
from wagtail.images.blocks import ImageBlock


class CardValueBlock(StructValue):

    def tags_list(self):
        tags = self.get('tags', None)
        if tags:
            return tags.split(',')

class CardBlock(StructBlock):
    heading = CharBlock()
    description = RichTextBlock(features=["bold", "italic", "link"])
    tags = CharBlock(required=False, help_text="Enter comma-separated tags")


    class Meta:
        icon = "form"
        template = "portfolio/blocks/card_block.html"
        value_class = CardValueBlock

class PortfolioStreamBlock(BaseStreamBlock):
    card = CardBlock(group="Sections")
