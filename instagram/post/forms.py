from django import forms

__all__ = (
    'PostForm',
    'CommentForm',
)


class PostForm(forms.Form):
    photo = forms.ImageField(
        required=True,
        widget=forms.ClearableFileInput(
            attrs={
                'class': 'form-control',
            }
        ),
    )
    # text를 받을 수 있는 필드 추가
    text = forms.CharField(
        max_length=5,
        widget=forms.TextInput(
            attrs={
                'class':'form-control',
            }
        ),
    )

    def clean_text(self):
        data = self.cleaned_data['text']
        if data != data.upper():
            raise forms.ValidationError('All text must uppercase!')
        return data


class CommentForm(forms.Form):
    content = forms.CharField(
        # 엔터 허용 widget 옵션
        widget=forms.Textarea(
            attrs={
                'class': 'form-control',
            }
        ),
    )