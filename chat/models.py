from uuid import uuid4
from django.db import models


class Visitor(models.Model):
    name = models.CharField(max_length=100)

    def __str__(self):
        return self.name


class Chat(models.Model):
    uuid = models.UUIDField(primary_key=True, default=uuid4, editable=False)
    name = models.CharField(max_length=100)
    max_visitors = models.IntegerField(default=4)
    visitors = models.ManyToManyField(Visitor)
    messages = models.TextField()

    def __str__(self):
        return self.name

    def possible_to_add(self):
        return len(self.visitors.all()) < self.max_visitors

    def add_visitor(self, visitor):
        self.visitors.add(visitor)
        self.save()

    def remove_visitor(self, visitor):
        self.visitors.remove(visitor)
        self.save()

    def add_message(self, message):
        self.messages += f"\n{message}"
        self.save()

    def excludes_if_must(self):
        if len(self.visitors.all()) == 0:
            self.delete()
