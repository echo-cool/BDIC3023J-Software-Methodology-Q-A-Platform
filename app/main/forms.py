from flask_wtf import FlaskForm
from flask_wtf.file import FileField, FileRequired, FileAllowed
from wtforms import StringField, SubmitField, TextAreaField, HiddenField
from wtforms.validators import DataRequired, Length


class NameForm(FlaskForm):
    name = StringField('What is your name?', validators=[DataRequired()])
    submit = SubmitField('Submit')


# 编辑、修改个人资料的表单设计
class EditProfileForm(FlaskForm):
    username = StringField('username', validators=[Length(0, 64)])
    college = StringField('college', validators=[Length(0, 10)])
    grade = StringField('grade', validators=[Length(0, 4)])
    about_me = TextAreaField('About me')
    submit = SubmitField('Submit')


# 帖子编辑的表单设计
class PostMdForm(FlaskForm):
    body = TextAreaField("Body", validators=[DataRequired()])
    body_html = HiddenField()


# 上传头像表单设计
class UploadPhotoForm(FlaskForm):
    photo = FileField('image', validators=[FileRequired(), FileAllowed(['jpg', 'png'], 'Images only!')])
    submit = SubmitField('Upload')


# 评论（回答）区的表单设计
class CommentForm(FlaskForm):
    body = TextAreaField('Enter your comment', render_kw={"placeholder": "Enter your comment"}, validators=[DataRequired()])
    submit = SubmitField('Submit')
