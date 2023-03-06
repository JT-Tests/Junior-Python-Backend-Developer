from django.db import models
from django.utils.safestring import mark_safe


class Menu(models.Model):
    slug = models.SlugField(max_length=50, unique=True, primary_key=True)
    title = models.CharField(max_length=50)

    def get_sorted(self, active=None):
        return Tree.get_sorted(self, active, not active)

    def get_sorted_all(self):
        return Tree.get_sorted(self)

    def __str__(self) -> str:
        return self.title

    class Meta:
        verbose_name = "menu"
        verbose_name_plural = "Menus"


class Tree(models.Model):
    title = models.CharField(max_length=50)
    menu = models.ForeignKey(
        Menu,
        on_delete=models.CASCADE,
        related_name="tree",
    )
    parent = models.ForeignKey(
        "self",
        on_delete=models.SET_NULL,
        blank=True,
        null=True,
        related_name="children",
    )

    @classmethod
    def get_sorted(cls, menu=None, active=None, finished=False):
        pk_list = cls.get_ids_list(menu, active, finished)

        preserved = models.Case(
            *[models.When(pk=pk, then=pos) for pos, pk in enumerate(pk_list)]
        )
        query = cls.objects.filter(pk__in=pk_list).order_by(preserved)
        return query

    def get_indent_level(self):
        level = 0
        node = self
        while True:
            if node.parent:
                node = node.parent
                level += 1
            else:
                break
        return level

    def get_child_ids(self, active=None, finished=False) -> list:
        ids_list = []
        last = self.id == active  # type: ignore
        for c in self.children.all():  # type: ignore
            if c.id == active:  # type: ignore
                last = True
            if finished:
                ids_list.append(c.id)  # type: ignore
            else:
                result, finished = c.get_child_ids(active, finished)
                ids_list += result
            if last:
                last = None
                finished = True
        return [self.id, *ids_list], finished  # type: ignore

    @classmethod
    def get_ids_list(cls, menu=None, active=None, finished=False):
        ids_list = []
        tree = cls.objects.filter(menu=menu) if menu else cls.objects.all()
        for i in tree.filter(parent=None):
            if active in i.get_child_ids()[0]:  # type: ignore
                finished = True
                result, _ = i.get_child_ids(active)
                ids_list += result
            elif finished:
                ids_list.append(i.id)  # type: ignore
            else:
                result, _ = i.get_child_ids()
                ids_list += result

        return ids_list

    @classmethod
    def get_draw_data(cls):
        pass

    @property
    def indent_name(self) -> str:
        breaks = f"|{'&nbsp' * 12}" * self.get_indent_level()
        return mark_safe(f"{breaks}{self.title}")

    def __str__(self) -> str:
        return self.title

    class Meta:
        verbose_name = "item"
        verbose_name_plural = "Tree"
