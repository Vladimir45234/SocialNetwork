from flask import render_template, url_for, flash, redirect, request, abort, Blueprint
from flaskblog import app, db, bcrypt
from flaskblog.forms import RegistrationForm, LoginForm, UpdateAccountForm, PostForm, UpdatePostForm, AddCommentForm, UpdateCommentForm
from flaskblog.models import User, Post, Comment, load_all_users
from flask_login import login_user, current_user, logout_user, login_required
from flaskblog.utils import save_picture, save_picture_post


users = Blueprint('user', __name__, template_folder='templates')

@app.route("/", methods=['GET', 'POST'])
@app.route("/home", methods=['GET', 'POST'])
@login_required
def home():
    form = PostForm()
    comment_form = AddCommentForm()
    user_id = db.session.query(User).count()
    page = request.args.get('page', 1, type=int)
    posts = Post.query.order_by(Post.date_posted.desc()).paginate(page=page, per_page=5)
    if form.validate_on_submit():
        if form.postpicture.data:
            post_image = save_picture_post(form.postpicture.data)
        post = Post(title=form.title.data, content=form.content.data, author=current_user, post_image=post_image)
        db.session.add(post)
        db.session.commit()
        flash('Ваш пост был создан!', 'success')
        return redirect(url_for('home'))
    post_file = url_for('static', filename='post_pics/' + Post.post_image)
    return render_template('home.html', posts=posts, user_id=user_id, form=form, post_file=post_file, comment_form=comment_form, page=page)


@app.route("/register", methods=['GET', 'POST'])
def register():
    user_id = db.session.query(User).count()
    if current_user.is_authenticated:
        return redirect(url_for('home'))
    form = RegistrationForm()
    if form.validate_on_submit():
        hashed_password = bcrypt.generate_password_hash(form.password.data).decode('utf-8')
        user = User(username=form.username.data, email=form.email.data, password=hashed_password)
        db.session.add(user)
        db.session.commit()
        if user:
            flash('Ваш аккаунт был создан. Пожалуйста, войдите', 'success')
            return redirect(url_for('login'))
        else:
            flash("Ошибка при добавлении в БД", "error")
    return render_template('register.html', title='Регисттрация', form=form, user_id=user_id)


@app.route("/login", methods=['GET', 'POST'])
def login():
    user_id = db.session.query(User).count()
    if current_user.is_authenticated:
        return redirect(url_for('home'))
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(email=form.email.data).first()
        if user and bcrypt.check_password_hash(user.password, form.password.data):
            login_user(user, remember=form.remember.data)
            next_page = request.args.get('next')
            return redirect(next_page) if next_page else redirect(url_for('home'))
        else:
            flash('Войти не удалось. Пожалуйста, проверьте адрес электронной почты и пароль', 'danger')
    return render_template('login.html', title='Авторизация', form=form, user_id=user_id)



@app.route("/logout")
def logout():
    logout_user()
    return redirect(url_for('home'))


@app.route("/account", methods=['GET', 'POST'])
@login_required
def account():
    form = UpdateAccountForm()
    user_id = db.session.query(User).count()
    if form.validate_on_submit():
        if form.picture.data:
            picture_file = save_picture(form.picture.data)
            current_user.image_file = picture_file
        current_user.username = form.username.data
        current_user.email = form.email.data
        db.session.commit()
        flash('Ваш аккаунт был обновлён', 'success')
        return redirect(url_for('account'))
    elif request.method == 'GET':
        form.username.data = current_user.username
        form.email.data = current_user.email
    image_file = url_for('static', filename='profile_pics/' + current_user.image_file)
    return render_template('account.html', title='Аккаунт',
                           image_file=image_file, form=form, user_id=user_id)


@app.route("/user/<string:username>")
def user_posts(username):
    page = request.args.get('page', 1, type=int)
    user_id = db.session.query(User).count()
    user = User.query.filter_by(username=username).first_or_404()
    posts = Post.query.filter_by(author=user)\
        .order_by(Post.date_posted.desc())\
        .paginate(page=page, per_page=5)
    return render_template('user_posts.html', posts=posts, user=user, user_id=user_id)




@app.route("/post/<int:post_id>", methods=['GET', 'POST'])
def post(post_id):
    post = Post.query.get_or_404(post_id)
    user_id = db.session.query(User).count()
    comment = Comment.query.filter_by(post_id=post.id).order_by(db.desc(Comment.date_comment)).all()
    post.views += 1
    db.session.commit()
    commentform = AddCommentForm()
    if request.method == 'POST':
        if commentform.validate_on_submit():
            username = current_user.username
            comment = Comment(username=username, body=commentform.body.data, post_id=post.id)
            db.session.add(comment)
            db.session.commit()
            flash('Комментарий к посту был добавлен', "success")
            return redirect(url_for('post', post_id=post.id))
    return render_template('post.html', title=post.title, post=post, post_id=post.id, commentform=commentform, comment=comment, user_id=user_id)


@app.route("/post/<int:post_id>/update", methods=['GET', 'POST'])
@login_required
def update_post(post_id):
    user_id = db.session.query(User).count()
    post = Post.query.get_or_404(post_id)
    page = request.args.get('page', 1, type=int)
    posts = Post.query.order_by(Post.date_posted.desc()).paginate(page=page, per_page=5)

    if post.author != current_user:
        abort(403)
    form = UpdatePostForm()
    if request.method == 'GET':
        form.title.data = post.title
        form.content.data = post.content
    if form.validate_on_submit():
        post.title = form.title.data
        post.content = form.content.data
        if form.postpicture.data:
            post.post_image = save_picture_post(form.postpicture.data)
        db.session.commit()
        flash('Ваш пост был обновлён!', 'success')
        return redirect(url_for('home', post_id=post.id))

    return render_template('home.html', title='Обновить пост',
                           form=form, legend='Обновить пост', user_id=user_id, posts=posts, page=page)


@app.route("/post/<int:post_id>/delete", methods=['POST'])
@login_required
def delete_post(post_id):
    post = Post.query.get_or_404(post_id)
    if post.author != current_user:
        abort(403)
    db.session.delete(post)
    db.session.commit()
    flash('Ваш пост был удалён!', 'success')
    return redirect(url_for('home'))

@app.route('/comment/<int:comment_id>/update', methods=['GET', 'POST'])
@login_required
def update_comment(comment_id):
    comment = Comment.query.get_or_404(comment_id)
    user_id = db.session.query(User).count()
    updatecommentform = UpdateCommentForm()
    if request.method == 'GET':
        updatecommentform.body.data = comment.body

    if updatecommentform.validate_on_submit():
        comment.body = updatecommentform.body.data
        db.session.commit()
        return redirect(url_for('post', post_id=comment.post_id))
    return render_template('update_comment.html', updatecommentform=updatecommentform, user_id=user_id)

@app.route('/comment/<int:comment_id>/delete')
@login_required
def delete_comment(comment_id):
    single_comment = Comment.query.get_or_404(comment_id)
    db.session.delete(single_comment)
    db.session.commit()
    flash('Комментарий был удалён', 'success')
    return redirect(url_for('post', post_id=single_comment.post_id))

@app.route('/like/<int:post_id>/<action>')
@login_required
def like_action(post_id, action):
    post = Post.query.filter_by(id=post_id).first_or_404()
    if action == 'like':
        current_user.like_post(post)
        db.session.commit()
    if action == 'unlike':
        current_user.unlike_post(post)
        db.session.commit()
    return redirect(request.referrer)

@app.route("/all_users")
def all_users():
    users = load_all_users()
    user_id = db.session.query(User).count()
    return render_template('all_users.html', user_id=user_id, userlist=users)

