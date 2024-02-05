from django import forms

class MatrixForm(forms.Form):  # クラス名を修正
    my_field = forms.IntegerField(label = 'Enter integer')