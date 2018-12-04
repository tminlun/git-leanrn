from django import forms
from django.contrib.contenttypes.models import ContentType
from django.db.models import ObjectDoesNotExist
from ckeditor.widgets import CKEditorWidget

class CommentForm(forms.Form):
    text = forms.CharField(required=True, widget=CKEditorWidget(config_name='comment_ckeditor'),
                           error_messages={'required': '评论内容不能为空'}
                           )
    content_type = forms.CharField(widget=forms.HiddenInput)
    object_id = forms.IntegerField(widget=forms.HiddenInput)

    # 初始化(*args:可以接收任意类型，是一个元组。**kwargs：必须要key和vault，是一个字典)
    def __init__(self, *args, **kwargs):
        if 'user' in kwargs:  # 判断pop是否有参数，
            self.user = kwargs.pop('user')  # 去掉kwargs, 把user传给super(如果用get会把user赋值给kwargrs)
        super(CommentForm, self).__init__(*args, **kwargs)  # CommentForm隐藏的初始化方法

    def clean(self):
        #判断用户是否登录,不管前端是否写了用户是否登录，到时候要前后端分离,按照原则判断是否登录要写在后端
        if not self.user.is_authenticated:
            raise forms.ValidationError('用户没登录')
        else:
            self.cleaned_data['user'] = self.user #传给forms / cleaned_data（即传给views）

        # text = self.cleaned_data['text'].strip()
        # if text == '':
        #     raise forms.ValidationError('输入内容不能为空')
        content_type = self.cleaned_data['content_type']
        object_id = self.cleaned_data['object_id']
        # 获取具体的对象
        try:
            model_class = ContentType.objects.get(model=content_type).model_class()  # class
            obj = model_class.objects.get(pk=object_id)
            self.cleaned_data['content_object'] = obj  # 传给views
        except ObjectDoesNotExist:
            raise forms.ValidationError('获取不到对象')
        return self.cleaned_data
