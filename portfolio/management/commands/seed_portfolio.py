from django.core.management.base import BaseCommand
from django.db import transaction

from home.models import HomePage, HomePageSkill
from portfolio.models import (
    ArticleIndexPage,
    ArticlePage,
    ContactPage,
    ExperienceBullet,
    ExperienceItem,
    ProjectIndexPage,
    ProjectPage,
    ProjectTechTag,
    TalkIndexPage,
    TalkTopic,
)


class Command(BaseCommand):
    help = (
        "Populates the homepage and creates the Projects / Speaking / Writing / Contact "
        "sections with the starter content from the original static portfolio design. "
        "Safe to run once on a fresh database; skips anything that already exists."
    )

    @transaction.atomic
    def handle(self, *args, **options):
        home = HomePage.objects.first()
        if home is None:
            self.stderr.write(self.style.ERROR("No HomePage found — run migrate first."))
            return

        home.title = "Holland"
        home.draft_title = "Holland"
        home.home_subtitle = "Naftali Holland"
        home.hero_heading = (
            "About"
        )
        home.about_text = (
            "<p>I'm a full-stack software engineer who moves between frontend and backend "
            "depending on what the problem needs. Lately that's meant dashboards and data "
            "tables in React and TypeScript, and service architecture, data modeling, and "
            "APIs in Django and Go.</p>"
            "<p>Most of my day-to-day work is building internal tooling for a real-time "
            "gaming platform — reporting dashboards, transaction views, and the reusable "
            "patterns underneath them. Outside of that, I care about backend fundamentals "
            "and infrastructure with real utility, particularly problems specific to the "
            "African context — mobile money, distributed systems for low-connectivity "
            "environments, and tools that don't assume the same defaults most software does.</p>"
            "<p>I work without much formal engineering mentorship day to day, so a good part "
            "of my growth has been self-directed — reading source code, studying how mature "
            "frameworks solve hard problems, and writing down what I learn along the way.</p>"
        )
        home.contact_heading = "Let's build something."
        home.contact_body = (
            "Open to conversations about engineering roles, collaboration, or anything "
            "backend-and-Africa shaped."
        )
        home.save()

        if not home.skills.exists():
            for name in ["React", "TypeScript", "Django", "Go", "PostgreSQL", "TanStack Query/Table"]:
                HomePageSkill.objects.create(page=home, name=name)
            self.stdout.write("Added skill tags")

        if not ExperienceItem.objects.exists():
            item = ExperienceItem.objects.create(
                role="Full Stack Developer",
                organisation="Softspin Technologies",
                date_range="2026 — present",
                summary=(
                    "Full-stack engineer maintaining the server side of a casino game and "
                    "building the frontend for a betting platform's backoffice."
                ),
                sort_order=0,
            )
            for text in [
                "Maintain and extend the Django backend of a live casino game.",
                "Built the React frontend for a betting platform's internal backoffice.",
                "Handle everyday feature work end to end across the stack.",
            ]:
                ExperienceBullet.objects.create(item=item, text=text)

            item2 = ExperienceItem.objects.create(
                role="Software Engineer",
                organisation="Inbet — iGames Platform",
                date_range="Previous role",
                summary=(
                    "Built and maintained gambling games and an internal admin dashboard "
                    "for a real-time gaming platform."
                ),
                sort_order=1,
            )
            for text in [
                "Built/maintained games including Aviator, Silver Jackpot, Froggy, and Nganya.",
                "Built the admin dashboard used daily by operations teams.",
                "Established reusable frontend patterns — pagination, filters, export, status badges.",
            ]:
                ExperienceBullet.objects.create(item=item2, text=text)
            self.stdout.write("Added experience timeline")

        if ProjectIndexPage.objects.first() is None:
            projects_index = ProjectIndexPage(
                title="Work",
                slug="work",
                intro=(
                    "<p>A mix of shipped platform tooling, work in progress, and personal "
                    "explorations — mostly React/TypeScript on the frontend, Django and Go "
                    "on the backend.</p>"
                ),
            )
            home.add_child(instance=projects_index)
            projects_index.save_revision().publish()

            sample_projects = [
                dict(
                    title="iGames Admin Dashboard",
                    status="shipped",
                    featured=True,
                    summary=(
                        "A React/TypeScript admin suite for a real-time gaming platform — "
                        "hierarchical account management, transaction views, and a reusable "
                        "export system built on a strategy pattern."
                    ),
                    tags=["React", "TanStack Table", "shadcn/ui"],
                ),
                dict(
                    title="Kiron Analytics & Transactions",
                    status="shipped",
                    featured=True,
                    summary=(
                        "A transactions table and analytics dashboard with a detail sheet "
                        "resilient to sparse API data, and proportional bar visualizations "
                        "built without a charting library."
                    ),
                    tags=["TypeScript", "TanStack Query", "date-fns"],
                ),
                dict(
                    title="Roll Tracker",
                    status="in_progress",
                    featured=True,
                    summary=(
                        "A digital replacement for a paper-based agent roll-request system — "
                        "REST API, data models, and an audit trail."
                    ),
                    tags=["Go", "GORM", "PostgreSQL"],
                ),
                dict(
                    title="Crash Game Simulation",
                    status="prototype",
                    featured=True,
                    summary=(
                        "A frontend simulation of a real-time 'crash' game built with PixiJS, "
                        "exploring rendering performance ahead of a planned WebSocket backend."
                    ),
                    tags=["React", "PixiJS", "Tailwind"],
                ),
                dict(
                    title="African Infrastructure Explorations",
                    status="concept",
                    featured=False,
                    summary=(
                        "Ongoing side explorations into backend problems specific to African "
                        "contexts: mobile money aggregation, a distributed task queue, and "
                        "SMS-based edtech."
                    ),
                    tags=["Go", "Django", "Systems design"],
                ),
            ]
            for data in sample_projects:
                project = ProjectPage(
                    title=data["title"],
                    status=data["status"],
                    featured=data["featured"],
                    summary=data["summary"],
                )
                projects_index.add_child(instance=project)
                project.save_revision().publish()
                for tag in data["tags"]:
                    ProjectTechTag.objects.create(page=project, name=tag)
            self.stdout.write("Added Work section with sample projects")
        else:
            projects_index = ProjectIndexPage.objects.first()

        if TalkIndexPage.objects.first() is None:
            talks_index = TalkIndexPage(
                title="Speaking",
                slug="speaking",
                empty_state_heading="I'm looking for my first talk.",
                empty_state_body=(
                    "If you run a meetup, a lunch-and-learn, or a small conference and think "
                    "one of the topics below would be a fit, I'd love to hear from you."
                ),
            )
            home.add_child(instance=talks_index)
            talks_index.save_revision().publish()

            topics = [
                (
                    "Building dashboard tooling that survives real-world APIs",
                    "Patterns for pagination, filtering, and export that hold up when the "
                    "backend doesn't play by the rules.",
                ),
                (
                    "Growing as an engineer without a mentor in the room",
                    "What self-directed technical growth looks like day to day.",
                ),
                (
                    "Infrastructure that assumes Africa, not Silicon Valley",
                    "Why mobile money, connectivity, and cost constraints change how you "
                    "design backend systems.",
                ),
            ]
            for title, description in topics:
                TalkTopic.objects.create(page=talks_index, title=title, description=description)
            self.stdout.write("Added Speaking section")

        if ArticleIndexPage.objects.first() is None:
            writing_index = ArticleIndexPage(
                title="Writing",
                slug="writing",
                intro=(
                    "<p>Nothing published yet — but writing down what I learn is part of how "
                    "I learn it, so this page is where that ends up.</p>"
                ),
            )
            home.add_child(instance=writing_index)
            writing_index.save_revision().publish()

            planned_articles = [
                dict(
                    title="Inside django.contrib.auth: the three strategy lists that hold it together",
                    summary=(
                        "A close read of Django's auth package and why treating its backend, "
                        "hasher, and validator settings as pluggable strategy lists is the key "
                        "to understanding the whole module."
                    ),
                ),
                dict(
                    title="TanStack Table's meta API: passing state into cell renderers cleanly",
                    summary=(
                        "The pattern I landed on for getting setters and callbacks into cell "
                        "renderers without prop drilling."
                    ),
                ),
                dict(
                    title="What backend infrastructure for Africa actually needs to assume",
                    summary=(
                        "Connectivity, cost, and mobile money change the defaults. Notes from "
                        "exploring mobile money aggregation and SMS-based edtech."
                    ),
                ),
            ]
            for data in planned_articles:
                article = ArticlePage(title=data["title"], status="planned", summary=data["summary"])
                writing_index.add_child(instance=article)
                article.save_revision().publish()
            self.stdout.write("Added Writing section")

        if ContactPage.objects.first() is None:
            contact = ContactPage(
                title="Contact",
                slug="contact",
                intro=(
                    "The best way to reach me is email — I read everything, even if I'm slow "
                    "to reply some weeks."
                ),
                location="Kenya · open to remote",
            )
            home.add_child(instance=contact)
            contact.save_revision().publish()
            self.stdout.write("Added Contact page (fill in your email/GitHub/LinkedIn in the admin)")

        self.stdout.write(self.style.SUCCESS("Portfolio seeded. Visit /admin/ to edit everything."))
