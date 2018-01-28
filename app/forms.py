# -*- coding: utf-8 -*-

from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField, SelectField, IntegerField,  DateField, DecimalField, SelectMultipleField
from wtforms.validators import DataRequired, Length, EqualTo
from flask_wtf.file import FileField,FileRequired,FileAllowed
from wtforms import ValidationError
from .models import User,load_department,Invoice

class NameForm(FlaskForm):
    id = IntegerField('OAid', validators=[DataRequired()])
    password = PasswordField('密码', validators=[DataRequired()])
    login = SubmitField('登录')

class AccountForm(FlaskForm):
    old_password = PasswordField('原密码', validators=[DataRequired()])
    password = PasswordField('新密码', validators=[
        DataRequired(), EqualTo('password2', message='两次密码输入不同')])
    password2 = PasswordField('确认新密码', validators=[DataRequired()])
    submit = SubmitField('修改')

class RegistrationForm(FlaskForm):
    username = StringField('姓名', validators=[DataRequired(), Length(1, 64)])
    id = IntegerField('OAid', validators=[DataRequired()])
    password = PasswordField('密码', validators=[
        DataRequired(), EqualTo('password2', message='两次密码输入不同')])
    password2 = PasswordField('确认密码', validators=[DataRequired()])
    department = SelectField('部门', validators=[DataRequired()], choices=[(0, '请选择部门')]+load_department(), coerce=int)
    submit = SubmitField('注册')

    def validate_id(self, field):
        if User.query.filter_by(id=field.data).first():
            raise ValidationError('OA 用户已注册。')

class AdminQueryForm(FlaskForm):
    departments=SelectMultipleField('部门', validators=[DataRequired()], choices=[(0, '公司全部')]+load_department(), coerce=int)
    submit = SubmitField('查询')

class UploadForm(FlaskForm):
    avatar = FileField(label=u'电子发票文件', validators=[FileRequired(),
                                                FileAllowed(['pdf','jpg', 'png'], message='只支持pdf/jpg/png!')])
    upload = SubmitField('上传')

class InvoiceRegisterForm(FlaskForm):
    code = StringField("发票代码", validators=[DataRequired()])
    num=StringField("发票号码",validators=[DataRequired()])
    date = DateField('开票日期', validators=[DataRequired()],format='%Y%m%d')
    check_code=StringField('校验码',validators=[DataRequired()])
    cost=DecimalField('金额(元)',validators=[DataRequired()],places=2)
    attach_cost=DecimalField('附单合计金额',validators=[DataRequired()],places=2)
    submit = SubmitField('登记')

    def validate_num(self, field):
        if Invoice.query.filter_by(number=field.data).first():
            raise ValidationError('请勿重复登记。')

    def validate_attach_cost(self,field):
        if field.data < self.cost.data:
            raise ValidationError('附单金额应大于发票金额')