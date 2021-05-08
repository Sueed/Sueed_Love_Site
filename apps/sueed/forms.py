from django import forms


class ContactForm(forms.Form):
    first_name = forms.CharField()
    last_name = forms.CharField()
    from_email = forms.EmailField()  # 发件方
    subject = forms.CharField()
    message = forms.CharField()
