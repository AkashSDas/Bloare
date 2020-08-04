from django import forms


# ****** Comment Form ******
class CommentForm(forms.Form):

    content_type = forms.CharField(widget=forms.HiddenInput)
    object_id = forms.IntegerField(widget=forms.HiddenInput)
    # parent_id = forms.IntegerField(widget=form.HiddenInput, required=False)
    content = forms.CharField(label="", widget=forms.Textarea)
