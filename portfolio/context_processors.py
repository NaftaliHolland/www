def nav_pages(request):
    """Make the main section index pages available to every template for nav links."""
    from home.models import HomePage
    from portfolio.models import ArticleIndexPage, ContactPage, ProjectIndexPage, TalkIndexPage

    return {
        "nav_home": HomePage.objects.live().first(),
        "nav_projects": ProjectIndexPage.objects.live().first(),
        "nav_talks": TalkIndexPage.objects.live().first(),
        "nav_writing": ArticleIndexPage.objects.live().first(),
        "nav_contact": ContactPage.objects.live().first(),
    }
