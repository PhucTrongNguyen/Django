from django import forms
from core.models import DanhGiaSP

class DanhGiaSPForm(forms.ModelForm):
    review = forms.CharField(widget=forms.Textarea(attrs={'placeholder':'Write review', 'class':'form-control'}))

    class Meta:
        model = DanhGiaSP
        fields = ['review','xepHang']