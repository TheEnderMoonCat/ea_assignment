from datetime import datetime
from flask import render_template, flash, redirect, url_for, request, g
from flask_login import login_user, logout_user, current_user, login_required
from werkzeug.urls import url_parse
from flask_babel import _, get_locale
from app import app, db
from app.forms import LoginForm, RegistrationForm, EditProfileForm, \
    ResetPasswordRequestForm, ResetPasswordForm, ProductForm, CompanysForm
from app.models import User, products, companys
from app.email import send_password_reset_email


@app.before_request
def before_request():
    if current_user.is_authenticated:
        current_user.last_seen = datetime.utcnow()
        db.session.commit()
    g.locale = str(get_locale())

@app.route('/', methods=['GET', 'POST'])
def index():
    productsout1 = products.query.filter_by(PID='1').all()
    productsout2 = products.query.filter_by(PID='2').all()
    productsout3 = products.query.filter_by(PID='3').all()
    row1 = companys.query.filter_by(CID='1').all()
    row2 = companys.query.filter_by(CID='2').all()
    row3 = companys.query.filter_by(CID='3').all()
    row4 = companys.query.filter_by(CID='4').all()
    row5 = companys.query.filter_by(CID='5').all()
    row6 = companys.query.filter_by(CID='6').all()
    tests = ['base_body.html', 'base.html']
    print(productsout1)
    print(row1)
    return render_template(tests,
                           productsout1=productsout1,
                           productsout2=productsout2,
                           productsout3=productsout3,
                           row1=row1, row2=row2, row3=row3, row4=row4, row5=row5, row6=row6)


@app.route('/login', methods=['GET', 'POST'])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(email=form.email.data).first()
        if user is None or not user.check_password(form.password.data):
            flash(_('Invalid email or password'))
            return redirect(url_for('login'))
        login_user(user, remember=form.remember_me.data)
        next_page = request.args.get('next')
        if not next_page or url_parse(next_page).netloc != '':
            next_page = url_for('index')
        return redirect(next_page)
    return render_template('login.html', title=_('Sign In'), form=form)

@app.route('/admin/<username>')
@login_required
def admin():
    admin = User.query.filter_by(admin='True').first_or_404()
    return render_template('base_body.html', admin=admin)

@app.route('/logout')
@login_required
def logout():
    logout_user()
    flash('You were logged out.')
    return redirect(url_for('index'))


@app.route('/register', methods=['GET', 'POST'])
def register():
    if current_user.is_authenticated:
        return redirect(url_for('index'))
    form = RegistrationForm()
    if form.validate_on_submit():
        user = User(username=form.username.data, email=form.email.data)
        user.set_password(form.password.data)
        db.session.add(user)
        db.session.commit()
        flash(_('Congratulations, you are now a registered user!'))
        return redirect(url_for('index'))
    return render_template('register.html', title=_('Register'), form=form)


@app.route('/reset_password_request', methods=['GET', 'POST'])
def reset_password_request():
    if current_user.is_authenticated:
        return redirect(url_for('index'))
    form = ResetPasswordRequestForm()
    if form.validate_on_submit():
        user = User.query.filter_by(email=form.email.data).first()
        if user:
            send_password_reset_email(user)
        flash(
            _('Check your email for the instructions to reset your password'))
        return redirect(url_for('login'))
    return render_template('reset_password_request.html',
                           title=_('Reset Password'), form=form)


@app.route('/reset_password/<token>', methods=['GET', 'POST'])
def reset_password(token):
    if current_user.is_authenticated:
        return redirect(url_for('index'))
    user = User.verify_reset_password_token(token)
    if not user:
        return redirect(url_for('index'))
    form = ResetPasswordForm()
    if form.validate_on_submit():
        user.set_password(form.password.data)
        db.session.commit()
        flash(_('Your password has been reset.'))
        return redirect(url_for('login'))
    return render_template('reset_password.html', form=form)


@app.route('/user/<username>')
@login_required
def user(username):
    user = User.query.filter_by(username=username).first_or_404()
    return render_template('base_body.html', user=user)


@app.route('/edit_profile', methods=['GET', 'POST'])
@login_required
def edit_profile():
    form = EditProfileForm(current_user.username)
    if form.validate_on_submit():
        current_user.username = form.username.data
        current_user.about_me = form.about_me.data
        db.session.commit()
        flash(_('Your changes have been saved.'))
        return redirect(url_for('edit_profile'))
    elif request.method == 'GET':
        form.username.data = current_user.username
        form.about_me.data = current_user.about_me
    return render_template('edit_profile.html', title=_('Edit Profile'),
                           form=form)


@app.route('/follow/<username>')
@login_required
def follow(username):
    user = User.query.filter_by(username=username).first()
    if user is None:
        flash(_('User %(username)s not found.', username=username))
        return redirect(url_for('index'))
    if user == current_user:
        flash(_('You cannot follow yourself!'))
        return redirect(url_for('user', username=username))
    current_user.follow(user)
    db.session.commit()
    flash(_('You are following %(username)s!', username=username))
    return redirect(url_for('user', username=username))


@app.route('/unfollow/<username>')
@login_required
def unfollow(username):
    user = User.query.filter_by(username=username).first()
    if user is None:
        flash(_('User %(username)s not found.', username=username))
        return redirect(url_for('index'))
    if user == current_user:
        flash(_('You cannot unfollow yourself!'))
        return redirect(url_for('user', username=username))
    current_user.unfollow(user)
    db.session.commit()
    flash(_('You are not following %(username)s.', username=username))
    return redirect(url_for('user', username=username))


@app.route('/INProduct', methods=['GET', 'POST'])
def INproduct():
    inproduct = ProductForm()
    if inproduct.validate_on_submit():
        Product = products(PN=inproduct.PN.data,
                           PURL=inproduct.PURL.data,
                           URL=inproduct.URL.data,
                           loc=inproduct.loc.data,
                           Price=inproduct.Price.data,
                           UPPrice=inproduct.UPPrice.data,
                           Intro=inproduct.Intro.data)
        db.session.add(Product)
        db.session.commit()
        flash(_('Success!'))
        return redirect(url_for('INproduct'))
    return render_template('product.html', title=_('ProductForm'), inproduct=inproduct)

@app.route('/Companys', methods=['GET','POST'])
def Company():
    company = CompanysForm()
    if company.validate_on_submit():
        Company = companys(CName=company.CName.data,
                           CURL=company.CURL.data)
        db.session.add(Company)
        db.session.commit()
        flash(_('Success!'))
        return redirect(url_for('Company'))
    return render_template('companys.html', title=_('Add Companys'), company=company)







