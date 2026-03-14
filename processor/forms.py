from django import forms
from PIL import Image


class UploadForm(forms.Form):
    image = forms.ImageField()


class PresetForm(forms.Form):
    name = forms.CharField(max_length=100)
    dot_spacing = forms.IntegerField(initial=10, min_value=1)
    style = forms.ChoiceField(choices=[("classic", "Classic"), ("diamond", "Diamond"), ("line", "Line")])
    is_default = forms.BooleanField(required=False)


class PresetImportForm(forms.Form):
    json_data = forms.CharField(widget=forms.Textarea)


class BatchUploadForm(forms.Form):
    images = forms.FileField(widget=forms.ClearableFileInput(attrs={"allow_multiple_selected": True}))
    make_public = forms.BooleanField(required=False, label="Make all images public")

    def clean_images(self):
        files = self.files.getlist("images")
        if not files:
            raise forms.ValidationError("Please upload at least one image.")

        for f in files:
            try:
                f.seek(0)
                img = Image.open(f)
                img.verify()
                f.seek(0)
            except Exception:
                raise forms.ValidationError(f"{f.name} is not a valid image file.")

        return self.cleaned_data.get("images")
