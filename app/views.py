# -*- coding: utf-8 -*-
from flask import render_template, flash, redirect, url_for, request
from app import app, db, Invoicezbar
from .models import User, Invoice, Department
from .forms import NameForm, RegistrationForm, UploadForm, InvoiceRegisterForm, AdminQueryForm, AccountForm
from .decorators import admin_required
from flask_login import login_user, logout_user, current_user, login_required
from werkzeug.datastructures import CombinedMultiDict
from werkzeug.utils import secure_filename
import os
from datetime import datetime
from sqlalchemy import desc

basedir = os.path.abspath(os.path.dirname(__file__))


@app.route('/', methods=['GET', 'POST'])
def main():
    values = CombinedMultiDict([request.files, request.form])
    form = UploadForm(values)
    if form.validate_on_submit():
        avatar = form.avatar.data
        #filename = secure_filename(avatar.filename)
        filename = avatar.filename
        file_path = os.path.join(basedir,"static","files",str(current_user.id), filename)
        # 文件名是非常危险的
        avatar.save(file_path)
        app.logger.warn("%s upload file %s success" % (current_user.id, filename))
        return redirect(url_for("InvoiceRegister", filename=filename))
    return render_template('main.html', form=form)


@app.route('/login', methods=['GET', 'POST'])
def login():
    form = NameForm()
    user =User.query.filter_by(id = form.id.data).first()
    if form.validate_on_submit():
        if user is not None and user.verify_password(form.password.data):
            login_user(user,True)
            app.logger.warn("%s login success" % form.id.data)
            return redirect(url_for('main'))
        else:
            app.logger.warn("%s login failed" % form.id.data)
            flash('用户名或密码错误！')
    return render_template('login.html', form=form)


@app.route('/logout')
@login_required
def logout():
    app.logger.warn("%s logout" % current_user.id)
    logout_user()
    flash('退出成功。')
    return redirect(url_for('main'))


@app.route('/regist', methods=['GET', 'POST'])
def regist():
    form = RegistrationForm()
    if form.validate_on_submit():
        user = User(id=form.id.data,
                    username=form.username.data,
                    password=form.password.data,
                    department_id=form.department.data)
        db.session.add(user)
        db.session.commit()
        os.mkdir(os.path.join(basedir,"static","files",str(form.id.data)))
        app.logger.warn("%s regist success" % form.id.data)
        return redirect(url_for('login'))
    return render_template('register.html',form=form)


@app.route('/account', methods=['GET', 'POST'])
@login_required
def account():
    user = User.query.filter_by(id=current_user.id).first()
    form = AccountForm()
    if form.validate_on_submit():
        if user is not None and user.verify_password(form.old_password.data):
            user.password=form.password.data
            db.session.add(user)
            db.session.commit()
            flash('密码修改成功，请重新登录！')
            logout_user()
            return redirect(url_for('login'))
        else:
            flash('用户名或密码错误！')
            form.data.clear()
    return render_template('account.html', form=form)


@app.route('/InvoiceRegister/<string:filename>', methods=['GET', 'POST'])
@login_required
def InvoiceRegister(filename):
    form = InvoiceRegisterForm()
    if form.validate_on_submit():
        invoice=Invoice(number=form.num.data,
                        cost=form.cost.data,
                        attached_cost=form.attach_cost.data,
                        date=form.date.data,
                        check_code=form.check_code.data,
                        upload_date=datetime.now().date(),
                        user_id=current_user.id,
                        filename=filename,
                        code=form.code.data)
        db.session.add(invoice)
        db.session.commit()
        app.logger.warn("%s regist invoice %s success" % (current_user.id, form.num.data))
        flash('发票登记成功')
        return redirect(url_for('main'))
    load_file = ''
    if filename is not '#':
        if filename.endswith('.pdf'):
            load_file = 'pdf'
        else:
            load_file = 'img'
        # "发票代码","发票号码","金额","开票日期","校验码"
        invoiceinfo = Invoicezbar.getinfo(current_user.id, filename)
        if invoiceinfo[0] is not '':
            form.code.data=invoiceinfo[0]
            form.num.data=invoiceinfo[1]
            form.cost.data=float(invoiceinfo[2])
            form.date.data=datetime.strptime(invoiceinfo[3],'%Y%m%d').date()
            form.check_code.data=invoiceinfo[4]
            app.logger.warn("user %s's file %s analysis success" % (current_user.id, filename))
        else:
            flash('文件解析失败，请手动填写')
            app.logger.warn("user %s's file %s analysis failed" % (current_user.id, filename))
    return render_template('InvoiceRegister.html',form=form, load_file=load_file, filename=filename)


@app.route('/query')
@login_required
def query():
    invoices = Invoice.query.filter_by(user_id=current_user.id).order_by(desc(Invoice.upload_date)).all()
    return render_template('query.html', invoices=invoices)


@app.route('/adminquery', methods=['GET', 'POST'])
@login_required
@admin_required
def adminquery():
    form = AdminQueryForm()
    if form.validate_on_submit():
        invoicedate = []
        for d_id in form.departments.data:
            if d_id == 0:
                d_name="公司"
                d_invoices = Invoice.query.order_by(desc(Invoice.upload_date)).all()
            else:
                d_name = db.session.query(Department.department_name).filter_by(id=d_id).first()[0]
                d_invoices = Invoice.query.join(User).join(Department).\
                    filter(Department.id==d_id).order_by(desc(Invoice.upload_date)).all()
            invoicedate.append([d_name,d_invoices])
        return render_template('adminquery.html', form=form, incoicesdata=invoicedate)
    return render_template('adminquery.html', form=form)


@app.errorhandler(403)
def internal_error(error):
    return render_template('403.html'), 403

@app.errorhandler(404)
def internal_error(error):
    return render_template('404.html'), 404

@app.errorhandler(500)
def internal_error(error):
    db.session.rollback()
    return render_template('500.html'), 500