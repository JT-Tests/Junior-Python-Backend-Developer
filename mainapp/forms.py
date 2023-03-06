from django import forms
from .models import Tree


class TreeForm(forms.ModelForm):

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields["parent"].choices = [
            (x.id, x.indent_name) for x in Tree.get_sorted()  # type: ignore
        ]

    class Meta:
        model = Tree
        fields = "__all__"
        widgets = {
            "parent": forms.Select(
                attrs={"size": "4", "style": "height: 200px; min-width: 250px"}
            )
        }
