from django import forms
from ckeditor.widgets import CKEditorWidget

class Comment_Form(forms.Form):
    text = forms.CharField(widget=CKEditorWidget(config_name='comment_ckeditor'),error_messages={'required': '评论内容不能为空'})
    content_type = forms.CharField()
    object_id = forms.IntegerField()

