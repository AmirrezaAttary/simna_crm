from django.core.management.base import BaseCommand
from permissions.models import Feature, Role, RoleFeaturePermission


class Command(BaseCommand):

    def handle(self, *args, **kwargs):

        features = [
            ("deals", "معاملات", 1, "handshake", "deal-list"),
            ("view_column", "پایپ لاین", 2, "view_column", "pipeline-board"),
            ("contacts", "مخاطبین", 3, "people", "contact-list"),
            ("leads", "سرنخ‌ها", 4, "person_add", "lead-list"),
            ("activities", "فعالیت‌ها", 5, "person_add", "task-list"),
        ]

        for codename, name, order, icon, url_name in features:
            Feature.objects.get_or_create(
                codename=codename,
                defaults={
                    "name": name,
                    "oreder": order,
                    "icon":icon,
                    "url_name":url_name
                }
            )


        manager, _ = Role.objects.get_or_create(
            codename="manager",
            defaults={
                "name":"مدیر"
            }
        )


        for feature in Feature.objects.all():

            RoleFeaturePermission.objects.get_or_create(
                role=manager,
                feature=feature,
                defaults={
                    "can_view":True,
                    "can_add":True,
                    "can_edit":True,
                    "can_delete":True,
                    "scope":"all"
                }
            )


        self.stdout.write(
            self.style.SUCCESS(
                "Permissions created"
            )
        )