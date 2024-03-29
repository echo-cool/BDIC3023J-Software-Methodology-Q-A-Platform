import os
import smtplib
from datetime import datetime
from email.header import Header
from email.mime.text import MIMEText
from operator import or_
from flask import render_template, redirect, url_for, flash, request, \
    current_app, make_response, jsonify
from flask_login import login_required, current_user
from sqlalchemy.sql.functions import func
from werkzeug.utils import secure_filename

from . import main
from .forms import UploadPhotoForm, CommentForm, PostMdForm, ReportForm
from .. import db, csrf, cache
from ..email import send_email_text
from ..models import Permission, User, Post, Comment, Notification, Like, Transaction, Activity, Collect, Want, \
    Question, Savequestion, Saveanswer
from ..decorators import permission_required
from ..util import check_text


@main.route('/', methods=['GET', 'POST'])
# @cache.cached(timeout=30)
def index():
    """Get index page

    @@@
    ### args
    None

    ### request
    ```json
    None
    ```

    ### return
    ```json
    HTML Page
    ```
    @@@
    """
    if request.method == 'GET':
        with db.session.no_autoflush:
            page1 = request.args.get('page', 1, type=int)
            query1 = Post.query
            pagination1 = query1.order_by(Post.recent_activity.desc()).paginate(
                page1, per_page=current_app.config['FLASKY_POSTS_PER_PAGE'],
                error_out=False)
            posts1 = pagination1.items
            # hot
            for item in query1:
                item.important = 0
                com_num = db.session.query(func.count(Comment.id)).filter_by(post_id=item.id).scalar()
                li_num = db.session.query(func.count(Like.liker_id)).filter_by(liked_post_id=item.id).scalar()
                item.important = 7 * com_num + 3 * li_num
            hot = query1.order_by(Post.important.desc())
            li = Activity.query.filter_by(is_invalid=False)
            for item in li:
                item.important = 0
                li_num = db.session.query(func.count(Want.wanter_id)).filter_by(wanted_Activity_id=item.id).scalar()
                item.important = li_num
            hot_activity = li.order_by(Activity.important.desc())
            return render_template('index/index_posts.html', posts1=posts1, posts5=hot,
                                   pagination1=pagination1, hot_activity=hot_activity)
    else:
        inf = request.form["search"]
        return redirect(url_for('.query', content=inf))


@main.route('/trans/', methods=['GET', 'POST'])
def index_transaction():
    """Get all the  transactions

    @@@
    ### args
    None

    ### request
    ```json
    None
    ```

    ### return
    ```json
    HTML Page
    ```
    @@@
    """
    if request.method == 'GET':
        with db.session.no_autoflush:
            query2 = Transaction.query
            transactions = query2.order_by(Transaction.timestamp.desc())
            # hot
            query1 = Post.query
            for item in query1:
                item.important = 0
                com_num = db.session.query(func.count(Comment.id)).filter_by(post_id=item.id).scalar()
                li_num = db.session.query(func.count(Like.liker_id)).filter_by(liked_post_id=item.id).scalar()
                item.important = 7 * com_num + 3 * li_num
            hot = query1.order_by(Post.important.desc())
            li = Activity.query.filter_by(is_invalid=False)
            for item in li:
                item.important = 0
                li_num = db.session.query(func.count(Want.wanter_id)).filter_by(wanted_Activity_id=item.id).scalar()
                item.important = li_num
            hot_activity = li.order_by(Activity.important.desc())
            return render_template('index/index_transactions.html', transactions=transactions, posts5=hot,
                                   hot_activity=hot_activity)
    else:
        inf = request.form["search"]
        return redirect(url_for('.query', content=inf))


@main.route('/act/', methods=['GET', 'POST'])
def index_activity():
    if request.method == 'GET':
        with db.session.no_autoflush:
            query3 = Activity.query
            for activity in query3:
                if activity.activity_time < datetime.utcnow():
                    activity.is_invalid = True
                    db.session.add(activity)
                    db.session.commit()
            activities = query3.order_by(Activity.timestamp.desc())
            # hot
            query1 = Post.query
            for item in query1:
                item.important = 0
                com_num = db.session.query(func.count(Comment.id)).filter_by(post_id=item.id).scalar()
                li_num = db.session.query(func.count(Like.liker_id)).filter_by(liked_post_id=item.id).scalar()
                item.important = 7 * com_num + 3 * li_num
            hot = query1.order_by(Post.important.desc())
            li = Activity.query.filter_by(is_invalid=False)
            for item in li:
                item.important = 0
                li_num = db.session.query(func.count(Want.wanter_id)).filter_by(wanted_Activity_id=item.id).scalar()
                item.important = li_num
            hot_activity = li.order_by(Activity.important.desc())
            return render_template('index/index_activities.html', activities=activities, posts5=hot,
                                   hot_activity=hot_activity)
    else:
        inf = request.form["search"]
        return redirect(url_for('.query', content=inf))


@main.route('/foll/', methods=['GET', 'POST'])
def index_follow():
    if request.method == 'GET':
        # hot
        with db.session.no_autoflush:
            query1 = Post.query
            for item in query1:
                item.important = 0
                com_num = db.session.query(func.count(Comment.id)).filter_by(post_id=item.id).scalar()
                li_num = db.session.query(func.count(Like.liker_id)).filter_by(liked_post_id=item.id).scalar()
                item.important = 7 * com_num + 3 * li_num
            hot = query1.order_by(Post.important.desc())
            query4 = current_user.followed_posts
            posts4 = query4.order_by(Post.recent_activity.desc())
            li = Activity.query.filter_by(is_invalid=False)
            for item in li:
                item.important = 0
                li_num = db.session.query(func.count(Want.wanter_id)).filter_by(wanted_Activity_id=item.id).scalar()
                item.important = li_num
            hot_activity = li.order_by(Activity.important.desc())
            return render_template('index/index_follows.html', posts4=posts4, posts5=hot, hot_activity=hot_activity)
    else:
        inf = request.form["search"]
        return redirect(url_for('.query', content=inf))


@main.route('/query/<content>', methods=['GET', 'POST'])
def query(content):
    """Search in the database

    @@@
    ### args
    <content>

    ### request
    ```json
    None
    ```

    ### return
    ```json
    HTML Page
    ```
    @@@
    """
    if request.method == 'GET':
        print("get")
        inf = content
        search_result = "%" + inf + "%"
        result = Post.query.filter(or_(Post.title.like(search_result), Post.body.like(search_result)))
        for item in result:
            item.important = 0
            if (item.title is None):
                item.title = ""
            if (item.body is None):
                item.body = ""
            sentence = item.title + item.body
            counts = 0
            list1 = sentence.split(" ")
            for y in range(len(list1)):
                if list1[y].find(inf) != -1:
                    counts = counts + 1
            item.important = counts
        page = request.args.get('page', 1, type=int)
        pagination1 = result.order_by(Post.important.desc()).paginate(
            page, per_page=current_app.config['FLASKY_POSTS_PER_PAGE'],
            error_out=False)
        relevance = pagination1.items
        pagination2 = result.order_by(Post.timestamp.desc()).paginate(
            page, per_page=current_app.config['FLASKY_POSTS_PER_PAGE'],
            error_out=False)
        newest = pagination2.items
        for item in result:
            item.important = 0
            with db.session.no_autoflush:
                com_num = db.session.query(func.count(Comment.id)).filter_by(post_id=item.id).scalar()
            item.important = com_num
        pagination3 = result.order_by(Post.important.desc()).paginate(
            page, per_page=current_app.config['FLASKY_POSTS_PER_PAGE'],
            error_out=False)
        hottest = pagination3.items
        for item in result:
            item.important = 0
            sentence = item.title + item.body
            counts = 0
            list1 = sentence.split(" ")
            for y in range(len(list1)):
                if list1[y].find(inf) != -1:
                    counts = counts + 1
            with db.session.no_autoflush:
                com_num = db.session.query(func.count(Comment.id)).filter_by(post_id=item.id).scalar()
                li_num = db.session.query(func.count(Like.liker_id)).filter_by(liked_post_id=item.id).scalar()
            item.important = counts * 4 + 3 * com_num + 3 * li_num
        pagination4 = result.order_by(Post.important.desc()).paginate(
            page, per_page=current_app.config['FLASKY_POSTS_PER_PAGE'],
            error_out=False)
        combination = pagination4.items
        # print(show_newest + show_relevance + show_hottest)
        for item in result:
            item.important = 0
        return render_template('querypost.html', relevance=relevance, newest=newest, hottest=hottest,
                               combination=combination, title="Result of query", inf=inf, pagination1=pagination1,
                               pagination2=pagination2, pagination3=pagination3, pagination4=pagination4)
    if request.method == 'POST':
        inf = request.form["inf"]
        if inf == "":
            flash("Search content cannot be empty.")
            return render_template('querypost.html')
        search_result = "%" + inf + "%"
        print(search_result)
        # result = Post.query.filter(or_(Post.title.like(search_result), Post.body.like(search_result)))
        result = Post.query.filter(Post.body.like(search_result))
        for item in result:
            item.important = 0
            if(item.title is None):
                item.title=""
            sentence = item.title + item.body
            counts = 0
            list1 = sentence.split(" ")
            for y in range(len(list1)):
                if list1[y].find(inf) != -1:
                    counts = counts + 1
            item.important = counts
        page = request.args.get('page', 1, type=int)
        pagination1 = result.order_by(Post.important.desc()).paginate(
            page, per_page=current_app.config['FLASKY_POSTS_PER_PAGE'],
            error_out=False)
        relevance = pagination1.items
        pagination2 = result.order_by(Post.timestamp.desc()).paginate(
            page, per_page=current_app.config['FLASKY_POSTS_PER_PAGE'],
            error_out=False)
        newest = pagination2.items
        for item in result:
            item.important = 0
            with db.session.no_autoflush:
                com_num = db.session.query(func.count(Comment.id)).filter_by(post_id=item.id).scalar()
            item.important = com_num
        pagination3 = result.order_by(Post.important.desc()).paginate(
            page, per_page=current_app.config['FLASKY_POSTS_PER_PAGE'],
            error_out=False)
        hottest = pagination3.items
        for item in result:
            item.important = 0
            sentence = item.title + item.body
            counts = 0
            list1 = sentence.split(" ")
            for y in range(len(list1)):
                if list1[y].find(inf) != -1:
                    counts = counts + 1
            with db.session.no_autoflush:
                com_num = db.session.query(func.count(Comment.id)).filter_by(post_id=item.id).scalar()
                li_num = db.session.query(func.count(Like.liker_id)).filter_by(liked_post_id=item.id).scalar()
            item.important = counts * 4 + 3 * com_num + 3 * li_num
        pagination4 = result.order_by(Post.important.desc()).paginate(
            page, per_page=current_app.config['FLASKY_POSTS_PER_PAGE'],
            error_out=False)
        combination = pagination4.items
        # print(show_newest + show_relevance + show_hottest)
        for item in result:
            item.important = 0
        return render_template('querypost.html', relevance=relevance, newest=newest, hottest=hottest,
                               combination=combination, title="Result of query", inf=inf, pagination1=pagination1,
                               pagination2=pagination2, pagination3=pagination3, pagination4=pagination4)


@main.route('/query-user', methods=['GET', 'POST'])
def query_user():
    if request.method == 'GET':
        return render_template('queryuser.html')
    if request.method == 'POST':
        inf = request.form["user"]
        if inf == "":
            flash("Search content cannot be empty.")
            return render_template('queryuser.html')
        search_result = "%" + inf + "%"
        result = User.query.filter(or_(User.username.like(search_result), User.student_id.like(search_result)))
        page = request.args.get('page', 1, type=int)
        pagination = result.order_by(User.username.desc()).paginate(
            page, per_page=current_app.config['FLASKY_FOLLOWERS_PER_PAGE'],
            error_out=False)
        query = pagination.items
        return render_template('queryuser.html', query=query, title="Result of query", pagination=pagination, inf=inf)


@main.route('/query-transaction', methods=['GET', 'POST'])
def query_transaction():
    if request.method == 'GET':
        return render_template('querytransaction.html')
    if request.method == 'POST':
        inf = request.form["transaction"]
        if inf == "":
            flash("Search content cannot be empty.")
            return render_template('querytransaction.html')
        search_result = "%" + inf + "%"
        result = Transaction.query.filter(or_(Transaction.item_name.like(search_result),
                                              Transaction.item_describe.like(search_result)))
        page = request.args.get('page', 1, type=int)
        pagination = result.order_by(Transaction.timestamp.desc()).paginate(
            page, per_page=current_app.config['FLASKY_FOLLOWERS_PER_PAGE'],
            error_out=False)
        query = pagination.items
        return render_template('querytransaction.html', query=query, title="Result of query", pagination=pagination,
                               inf=inf)


@main.route('/user/<username>')
def user(username):
    """Get this user' information by username

    @@@
    ### args
    <username>

    ### request
    ```json
    None
    ```

    ### return
    ```json
    HTML Page
    ```
    @@@
    """
    user = User.query.filter_by(username=username).first_or_404()
    liking = Like.query.filter_by(liker_id=user.id)
    collecting = user.collected_transaction
    wanting = user.wanted_Activity

    posts = user.posts.order_by(Post.timestamp.desc())
    questions = user.questions.order_by(Question.timestamp.desc())
    concernQuestions = Savequestion.query.filter_by(saver_id=user.id)
    concernAnswers = Saveanswer.query.filter_by(saver_id=user.id)

    liking_posts = [{'post': item.liked_post, 'timestamp': item.timestamp} for item in
                    liking.order_by(Like.timestamp.desc())]
    transactions = user.transactions.order_by(Transaction.timestamp.desc())
    activities = user.activities.order_by(Activity.timestamp.desc())
    collects = collecting.order_by(Collect.timestamp.desc())
    wants = wanting.order_by(Want.timestamp.desc())
    return render_template('user.html', user=user, posts=posts, questions=questions, liking_posts=liking_posts,
                           activities=activities,
                           transactionsInProfile=transactions, collects=collects, wants=wants,
                           concernQuestions=concernQuestions, concernAnswers=concernAnswers)


@main.route('/notification')
def notification():
    """Get all the notifications

    @@@
    ### args
    None

    ### request
    ```json
    None
    ```

    ### return
    ```json
    HTML Page
    ```
    @@@
    """
    page = request.args.get('page', 1, type=int)
    pagination = current_user.notifications.order_by(Notification.timestamp.desc()).paginate(
        page, per_page=current_app.config['FLASKY_POSTS_PER_PAGE'],
        error_out=False)
    notices = pagination.items
    return render_template('table/notifications.html', notices=notices,
                           pagination=pagination)


@main.route('/change_read/<int:id>')
def change_read(id):
    """Change the read status of a notification

    @@@
    ### args
    <int:id> (Notification id)

    ### request
    ```json
    None
    ```

    ### return
    ```json
    redirect(url_for('.notification'))
    ```
    @@@
    """
    notice = Notification.query.filter_by(id=id).first()
    notice.is_read = True
    db.session.add(notice)
    db.session.commit()
    flash("You have read one notification")
    return redirect(url_for('.notification'))


ALLOWED_EXTENSIONS = set(['png', 'jpg', 'jpeg', 'gif'])


def allow_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS


@main.route('/photo', methods=['POST'])
def uploadPhoto():
    """Upload a image

    @@@
    ### args
    None

    ### request
    ImageData

    ### return
    ```json
    redirect(url_for('.edit_profile'))
    ```
    @@@
    """
    form = UploadPhotoForm()
    f = form.photo.data
    if f and allow_file(f.filename):
        filename = secure_filename(f.filename)
        f.save(os.path.join('app', 'static', 'assets', filename))
        current_user.avatar_img = '/static/assets/' + filename
        db.session.commit()
    else:
        flash("Please upload a picture of the compound rule")
    return redirect(url_for('.edit_profile'))


@main.route('/edit-profile', methods=['GET', 'POST'])
@login_required
def edit_profile():
    """Change user's profile

    @@@
    ### args
    None

    ### request
    ```json
    {
    username: "",
    collage: "",
    grade: "",
    aboutme: "",
    main_image_file: ""
    }
    ```

    ### return
    ```json
    redirect(url_for('.user', username=current_user.username))
    ```
    @@@
    """
    form = UploadPhotoForm()
    if request.method == 'GET':
        return render_template('edit_profile.html', form=form)
    if request.method == 'POST':
        # 读取前端数据
        try:
            main_image_file = form.main_image_file.data
            print(main_image_file)
            main_image_url = ""
            if main_image_file.filename != "":
                filename = str(os.urandom(30).hex()) + "." + main_image_file.filename.split(".")[-1]
                main_image_file.save(os.path.join(current_app.static_folder, 'assets', filename))
                main_image_url = filename
        except:
            pass
        username_find = User.query.filter_by(username=request.form["username"]).first()
        if username_find is not None and username_find != current_user:
            flash("Your new username already exists, please change your username")
            return render_template('edit_profile.html', form=form)

        current_user.username = request.form["username"]
        current_user.college = request.form["collage"]
        current_user.grade = request.form["grade"]
        current_user.about_me = request.form["aboutme"]
        db.session.add(current_user._get_current_object())
        db.session.commit()
        flash('Your profile has been updated.')
        return redirect(url_for('.user', username=current_user.username))


@main.route('/post/<int:id>', methods=['GET', 'POST'])
def post(id):
    post = Post.query.get_or_404(id)
    form = CommentForm()
    page = request.args.get('page', 1, type=int)
    if page == -1:
        page = (post.comments.count('*') - 1) // \
               current_app.config['FLASKY_COMMENTS_PER_PAGE'] + 1
    pagination = Comment.query.with_parent(post).order_by(Comment.timestamp.asc()).paginate(
        page, per_page=current_app.config['FLASKY_COMMENTS_PER_PAGE'],
        error_out=False)
    comments = pagination.items
    """发表评论与回复"""
    if form.validate_on_submit():
        body = form.body.data
        if request.form.get('anonymous') == "on":
            is_anonymous = True
            username = "Anonymous"
        else:
            is_anonymous = False
            username = current_user.username
        comment = Comment(body=body,
                          post=post,
                          author=current_user._get_current_object(),
                          replied_id=request.args.get('reply'),
                          is_anonymous=is_anonymous)
        comment.post.recent_activity = datetime.utcnow()
        if comment.replied_id:
            replied = Comment.query.get_or_404(comment.replied_id)
            comment.replied = replied
            action1 = " has replied<" + comment.body + "> to your comment<" + comment.replied.body + "> in the posting "
            n1 = Notification(receiver_id=comment.replied.author_id, timestamp=datetime.utcnow(),
                              username=username, action=action1,
                              object=" answer ", object_id=post.id)
            db.session.add(n1)
            db.session.commit()
            action2 = " has commented<" + comment.body + "> on your posting"
            n2 = Notification(receiver_id=post.author_id, timestamp=datetime.utcnow(),
                              username=username, action=action2,
                              object=" answer ", object_id=post.id)
            db.session.add(n2)
            db.session.commit()
        else:
            action = " has commented<" + comment.body + "> on your posting"
            """传入通知信息"""
            n = Notification(receiver_id=post.author_id, timestamp=datetime.utcnow(),
                             username=username, action=action,
                             object=" answer ", object_id=post.id)
            db.session.add(n)
            db.session.commit()
        db.session.add(comment)
        db.session.commit()
        if comment.is_anonymous:
            flash('Comment published anonymously')
        else:
            flash('Comment published successfully')
        return redirect(url_for('.post', id=post.id))
    # return render_template('answer.html', posts=[post], form=form, comments=comments, pagination=pagination)
    return render_template('post.html', posts=[post], form=form, comments=comments, pagination=pagination)


@main.route('/reply/comment/<int:comment_id>')
def reply_comment(comment_id):
    """作为中转函数通过URL传递被回复评论信息"""
    comment = Comment.query.get_or_404(comment_id)
    post1 = comment.post
    author = comment.author.username
    post1.recent_activity = datetime.utcnow()
    if comment.is_anonymous:
        author = "anonymous"
    db.session.commit()
    return redirect(url_for('.post', id=comment.post.id, reply=comment_id, author=author))


@main.route('/delete_comment/<int:id>')
@login_required
def delete_comment(id):
    comment = Comment.query.get_or_404(id)
    posts = Post.query.filter_by(id=comment.post_id).first()
    users = User.query.filter_by(id=posts.author_id).first()
    if current_user == comment.author or current_user == users:
        db.session.delete(comment)
        db.session.commit()
        flash('The comment has been deleted.')
        return redirect(url_for('.post', id=posts.id))
    else:
        flash('You do not have the rights to delete this comment')
        return redirect(url_for('.post', id=posts.id))


@main.route('/delete_post_profile/<post_id>')
@login_required
def delete_post_inProfile(post_id):
    post = Post.query.filter_by(id=post_id).first()
    db.session.delete(post)
    db.session.commit()
    flash('The posting has been deleted.')
    return redirect(url_for('.user', username=current_user.username))


@main.route('/delete_question_profile/<question_id>')
@login_required
def delete_question_inProfile(question_id):
    post = Question.query.filter_by(id=question_id).first()
    db.session.delete(post)
    db.session.commit()
    flash('The posting has been deleted.')
    return redirect(url_for('.user', username=current_user.username))


@main.route('/send_message/<username>/<message>')
@login_required
def send_message(username, message):
    currentUserObj: User = current_user
    user: User = User.query.filter_by(username=username).first()
    if user is None:
        flash('Invalid user.')
        return redirect(url_for('.index'))
    check = check_text(message)
    print(check)
    if check["conclusionType"] != 1:
        data = check['data'][0]["msg"]
        flash('Your message violated the rule of our web site. ' + message + " " + data)
        return redirect(url_for('.user', username=username))

    currentUserObj.send_message(user, message)
    db.session.commit()
    flash('You have sent:' + message + " To: " + username)
    return redirect(url_for('.user', username=username))


@main.route('/follow/<username>')
@login_required
@permission_required(Permission.FOLLOW)
def follow(username):
    user = User.query.filter_by(username=username).first()
    if user is None:
        flash('Invalid user.')
        return redirect(url_for('.index'))
    if current_user.is_following(user):
        flash('You have already followed this user.')
        return redirect(url_for('.user', username=username))
    current_user.follow(user)
    db.session.commit()
    flash('You are now following %s.' % username)
    return redirect(url_for('.user', username=username))

@main.route('/AJAXfollow/<username>', methods=['POST'], strict_slashes=False)
@csrf.exempt
@permission_required(Permission.FOLLOW)
def AJAXfollow(username):
    if current_user is None:
        return redirect(url_for("/"))
    user = User.query.filter_by(username=username).first()
    if user is not None:
        if current_user.is_following(user):
            current_user.unfollow(user)
            db.session.commit()
            return jsonify({'code': 200, 'like': False})
        else:
            current_user.follow(user)
            db.session.commit()
            return jsonify({'code': 200, 'like': True})


@main.route('/unfollow/<username>')
@login_required
@permission_required(Permission.FOLLOW)
def unfollow(username):
    user = User.query.filter_by(username=username).first()
    if user is None:
        flash('Invalid user.')
        return redirect(url_for('.index'))
    if not current_user.is_following(user):
        flash('You are not following this user.')
        return redirect(url_for('.user', username=username))
    current_user.unfollow(user)
    db.session.commit()
    flash('You do not follow %s anymore.' % username)
    return redirect(url_for('.user', username=username))


@main.route('/like/<post_id>')
@login_required
@permission_required(Permission.FOLLOW)
def like(post_id):
    post = Post.query.filter_by(id=post_id).first()
    if post is None:
        flash('Invalid post.')
        return redirect(url_for('.index'))
    if current_user.is_liking(post):
        flash('You have already gave a like to this post.')
        return redirect(url_for('.post', id=post_id))
    current_user.like(post)
    post.like(current_user)
    post.recent_activity = datetime.utcnow()
    db.session.commit()
    flash('You give a like to this answer')
    return redirect(url_for('.index', id=post_id))


@main.route('/AJAXlike/<post_id>', methods=['POST'], strict_slashes=False)
# @login_required
@csrf.exempt
@permission_required(Permission.FOLLOW)
def AJAXlike(post_id):
    if current_user is None:
        return redirect(url_for("/"))
    post = Post.query.filter_by(id=post_id).first()
    if post is not None:
        if current_user.is_liking(post):
            current_user.dislike(post)
            post.dislike(current_user)
            db.session.commit()
            return jsonify({'code': 200, 'like': False, 'num': post.liker.count()})
        else:
            current_user.like(post)
            post.like(current_user)
            post.recent_activity = datetime.utcnow()
            db.session.commit()
            return jsonify({'code': 200, 'like': True, 'num': post.liker.count()})


@main.route('/likeinpost/<post_id>')
@login_required
@permission_required(Permission.FOLLOW)
def like_inpost(post_id):
    post = Post.query.filter_by(id=post_id).first()
    if post is None:
        flash('Invalid post.')
        return redirect(url_for('.index'))
    if current_user.is_liking(post):
        flash('You are already liking this post.')
        return redirect(url_for('.post', id=post_id))
    current_user.like(post)
    post.like(current_user)
    post.recent_activity = datetime.utcnow()
    db.session.commit()
    flash('You are now liking this post')
    return redirect(url_for('.post', id=post_id))


@main.route('/dislike/<post_id>')
@login_required
@permission_required(Permission.FOLLOW)
def dislike(post_id):
    post = Post.query.filter_by(id=post_id).first()
    if post is None:
        flash('Invalid post.')
        return redirect(url_for('.index'))
    if not current_user.is_liking(post):
        flash('You are not liking this post.')
        return redirect(url_for('.post', id=post_id))
    current_user.dislike(post)
    post.dislike(current_user)
    db.session.commit()
    flash('You are not liking this post')
    return redirect(url_for('.index', id=post_id))


@main.route('/dislikeinpost/<post_id>')
@login_required
@permission_required(Permission.FOLLOW)
def dislike_inpost(post_id):
    post = Post.query.filter_by(id=post_id).first()
    if post is None:
        flash('Invalid post.')
        return redirect(url_for('.index'))
    if not current_user.is_liking(post):
        flash('You are not liking this post.')
        return redirect(url_for('.post', id=post_id))
    current_user.dislike(post)
    post.dislike(current_user)
    db.session.commit()
    flash('You are not liking this post')
    return redirect(url_for('.post', id=post_id))


# 显示所有followers的人
@main.route('/followers/<username>')
def followers(username):
    user = User.query.filter_by(username=username).first()
    if user is None:
        flash('Invalid user.')
        return redirect(url_for('.index'))
    page = request.args.get('page', 1, type=int)
    pagination = user.followers.paginate(
        page, per_page=current_app.config['FLASKY_FOLLOWERS_PER_PAGE'],
        error_out=False)
    follows = [{'user': item.follower, 'timestamp': item.timestamp}
               for item in pagination.items]
    return render_template('table/followers.html', user=user, title="Followers of",
                           endpoint='.followers', pagination=pagination,
                           follows=follows)


# 显示所有followed的人
@main.route('/followed_by/<username>')
def followed_by(username):
    user = User.query.filter_by(username=username).first()
    if user is None:
        flash('Invalid user.')
        return redirect(url_for('.index'))
    page = request.args.get('page', 1, type=int)
    pagination = user.following.paginate(
        page, per_page=current_app.config['FLASKY_FOLLOWERS_PER_PAGE'],
        error_out=False)
    follows = [{'user': item.followed, 'timestamp': item.timestamp}
               for item in pagination.items]
    return render_template('table/followers.html', user=user, title="Followed by",
                           endpoint='.followed_by', pagination=pagination,
                           follows=follows)


# 显示所有喜欢这个post的人
@main.route('/liked_by/<post_id>')
def liked_by(post_id):
    post = Post.query.filter_by(id=post_id).first()
    if post is None:
        flash('Invalid post.')
        return redirect(url_for('.index'))
    page = request.args.get('page', 1, type=int)
    pagination = post.liker.paginate(
        page, per_page=current_app.config['FLASKY_LIKER_PER_PAGE'],
        error_out=False)
    liker = [{'user': item.liker, 'timestamp': item.timestamp}
             for item in pagination.items]
    return render_template('table/liker.html', post=post, title="The liker of",
                           endpoint='.liked_by', pagination=pagination,
                           liker=liker)


@main.route('/new_post_md', methods=['GET', 'POST'])
@login_required
def new_post_md():
    form = PostMdForm()
    if current_user.can(Permission.WRITE) and form.validate_on_submit():
        title = request.form.get('title')
        body = form.body.data
        if request.form.get('anonymous') == "on":
            is_anonymous = True
        else:
            is_anonymous = False
        if title == "":
            flash("Title cannot be None!")
            return render_template('new_posting/new_mdpost.html', form=form)
        body_html = request.form['test-editormd-html-code']
        post = Post(title=title,
                    body=body,
                    body_html=body_html,
                    is_anonymous=is_anonymous,
                    author=current_user._get_current_object())
        post.recent_activity = datetime.utcnow()
        db.session.add(post)
        db.session.commit()
        if post.is_anonymous:
            flash("You have just posted a posting anonymously", 'success')
        else:
            flash("You have just posted a posting", 'success')
        return redirect(url_for('.index'))
    return render_template('new_posting/new_mdpost.html', form=form)


@main.route('/new_question_md', methods=['GET', 'POST'])
@login_required
def new_question_md():
    form = PostMdForm()
    if current_user.can(Permission.WRITE) and form.validate_on_submit():
        title = request.form.get('title')
        body = form.body.data
        if request.form.get('anonymous') == "on":
            is_anonymous = True
        else:
            is_anonymous = False
        if title == "":
            flash("Title cannot be None!")
            return render_template('new_posting/new_mdpost.html', form=form, default_body="", default_title="")
        body_html = request.form['test-editormd-html-code']
        question = Question(title=title,
                            body=body,
                            body_html=body_html,
                            is_anonymous=is_anonymous,
                            author=current_user._get_current_object())
        question.recent_activity = datetime.utcnow()
        db.session.add(question)
        db.session.commit()
        if question.is_anonymous:
            flash("You have just posted a question anonymously", 'success')
        else:
            flash("You have just posted a question", 'success')
        return redirect(url_for('.index'))
    return render_template('new_posting/new_mdquestion.html', form=form, default_body="", default_title="")


@main.route('/edit_question_md/<question_id>', methods=['GET', 'POST'])
@login_required
def edit_question_md(question_id):
    form = PostMdForm()
    question = Question.query.filter_by(id=question_id).first()
    if current_user.can(Permission.WRITE) and form.validate_on_submit():
        title = request.form.get('title')
        body = form.body.data
        if request.form.get('anonymous') == "on":
            is_anonymous = True
        else:
            is_anonymous = False
        if title == "":
            flash("Title cannot be None!")
            return render_template('new_posting/new_mdquestion.html', form=form, default_title=question.title,
                                   default_body=question.body)
        body_html = request.form['test-editormd-html-code']
        question.title = title
        question.body = body
        question.body_html = body_html
        question.is_anonymous = is_anonymous
        question.recent_activity = datetime.utcnow()
        db.session.add(question)
        db.session.commit()
        if question.is_anonymous:
            flash("You have just modified a question anonymously", 'success')
        else:
            flash("You have just modified a question", 'success')
        return redirect(url_for('.index'))
    return render_template('new_posting/new_mdquestion.html', form=form, default_title=question.title,
                           default_body=question.body)


@main.route('/new_answer_md/<question_id>', methods=['GET', 'POST'])
@login_required
def new_answer_md(question_id):
    form = PostMdForm()
    if current_user.can(Permission.WRITE) and form.validate_on_submit():
        title = request.form.get('title')
        body = form.body.data
        if request.form.get('anonymous') == "on":
            is_anonymous = True
        else:
            is_anonymous = False
        # if title == "":
        #     flash("Title cannot be None!")
        #     return render_template('new_posting/new_mdanswer.html', form=form)
        body_html = request.form['test-editormd-html-code']
        post = Post(title=title,
                    body=body,
                    body_html=body_html,
                    is_anonymous=is_anonymous,
                    author=current_user._get_current_object(),
                    question_id=question_id)
        post.recent_activity = datetime.utcnow()
        db.session.add(post)
        db.session.commit()
        if post.is_anonymous:
            flash("You have just posted an answer anonymously", 'success')
        else:
            flash("You have just posted an answer", 'success')
        return redirect(url_for('.view_question', question_id=question_id))
    return render_template('new_posting/new_mdanswer.html', form=form, default_body="")


@main.route('/edit_answer_md/<answer_id>', methods=['GET', 'POST'])
@login_required
def edit_answer_md(answer_id):
    form = PostMdForm()
    answer = Post.query.filter_by(id=answer_id).first()
    if current_user.can(Permission.WRITE) and form.validate_on_submit():
        title = request.form.get('title')
        body = form.body.data
        if request.form.get('anonymous') == "on":
            is_anonymous = True
        else:
            is_anonymous = False
        body_html = request.form['test-editormd-html-code']
        answer.title = title
        answer.body = body
        answer.body_html = body_html
        answer.is_anonymous = is_anonymous
        answer.recent_activity = datetime.utcnow()
        db.session.add(answer)
        db.session.commit()
        if answer.is_anonymous:
            flash("You have just modified an answer anonymously", 'success')
        else:
            flash("You have just modified an answer", 'success')
        return redirect(url_for('.index'))
    return render_template('new_posting/new_mdanswer.html', form=form,
                           default_body=answer.body)


@main.route('/questions/<question_id>', methods=['GET', 'POST'])
def view_question(question_id):
    if request.method == 'GET':
        with db.session.no_autoflush:
            question = Question.query.get_or_404(question_id)
            page1 = request.args.get('page', 1, type=int)
            query1 = Post.query
            pagination1 = query1.with_parent(question).order_by(Post.timestamp.asc()).paginate(
                page1, per_page=current_app.config['FLASKY_POSTS_PER_PAGE'],
                error_out=False)
            posts1 = pagination1.items
            # hot
            for item in query1:
                item.important = 0
                with db.session.no_autoflush:
                    com_num = db.session.query(func.count(Comment.id)).filter_by(post_id=item.id).scalar()
                    li_num = db.session.query(func.count(Like.liker_id)).filter_by(liked_post_id=item.id).scalar()
                item.important = 7 * com_num + 3 * li_num
            hot = query1.order_by(Post.important.desc())
            li = Activity.query.filter_by(is_invalid=False)
            for item in li:
                item.important = 0
                li_num = db.session.query(func.count(Want.wanter_id)).filter_by(wanted_Activity_id=item.id).scalar()
                item.important = li_num
            hot_activity = li.order_by(Activity.important.desc())
            return render_template('Posts/question.html', posts1=posts1, posts5=hot,
                                   pagination1=pagination1, hot_activity=hot_activity, question=question,
                                   question_id=question_id)
    else:
        inf = request.form["search"]
        return redirect(url_for('.query', content=inf))


@main.route('/savequestions/<question_id>')
def save_question(question_id):
    question = Question.query.filter_by(id=question_id).first()
    if question is None:
        flash('Invalid post.')
        return redirect(url_for('.index'))
    if current_user.is_savingquestion(question):
        flash('You are already liking this post.')
        return redirect(url_for('.post', id=question_id))
    current_user.savequestion(question)
    db.session.commit()
    flash('You are now liking this post')
    return redirect(url_for('.view_question', question_id=question_id))


@main.route('/AJAXsave_question/<question_id>', methods=['POST'], strict_slashes=False)
# @login_required
@csrf.exempt
@permission_required(Permission.FOLLOW)
def AJAXsave_question(question_id):
    if current_user is None:
        return redirect(url_for("/"))
    question = Question.query.filter_by(id=question_id).first()
    if question is not None:
        if current_user.is_savingquestion(question):
            current_user.unsavequestion(question)
            # question.dis...(current_user)
            db.session.commit()
            return jsonify({'code': 200, 'like': False, 'num': question.savers.count()})
        else:
            current_user.savequestion(question)
            db.session.commit()
            return jsonify({'code': 200, 'like': True, 'num': question.savers.count()})


@main.route('/AJAXsave_answer/<answer_id>', methods=['POST'], strict_slashes=False)
# @login_required
@csrf.exempt
@permission_required(Permission.FOLLOW)
def AJAXsave_answer(answer_id):
    if current_user is None:
        return redirect(url_for("/"))
    answer = Post.query.filter_by(id=answer_id).first()
    if answer is not None:
        if current_user.is_savinganswer(answer):
            current_user.unsaveanswer(answer)
            db.session.commit()
            return jsonify({'code': 200, 'like': False, 'num': answer.savers.count()})
        else:
            current_user.saveanswer(answer)
            db.session.commit()
            return jsonify({'code': 200, 'like': True, 'num': answer.savers.count()})


@main.route('/invitelist/<question_id>')
def invite_list(question_id):
    # user = User.query.filter_by(id=user_id).first()
    user = current_user
    if user is None:
        flash('Invalid user.')
        return redirect(url_for('.index'))
    page = request.args.get('page', 1, type=int)
    pagination = user.following.paginate(
        page, per_page=current_app.config['FLASKY_FOLLOWERS_PER_PAGE'],
        error_out=False)
    follows = [{'user': item.followed, 'timestamp': item.timestamp}
               for item in pagination.items]
    return render_template('table/invite.html', user=user, title="Followed by",
                           endpoint='.followed_by', pagination=pagination,
                           follows=follows, question_id=question_id)


@main.route('/invite/<question_id>/<user_id>')
def invite(question_id, user_id):
    question = Question.query.filter_by(id=question_id).first()
    user = User.query.filter_by(id=user_id).first()

    notification = Notification(timestamp=datetime.utcnow(), username=current_user.username, action=" has invited ",
                                object=question.title, object_id=question_id, receiver_id=user_id)
    db.session.add(notification)
    db.session.commit()
    return redirect(url_for('.invite_list', question_id=question_id))


@main.route('/report/<type>/<id>/', methods=['GET', 'POST'])
def report(type, id):
    form = ReportForm()
    if (request.method == 'POST'):
        url = ""
        user_url = url_for(".user", username=current_user.username)
        if (type == "answer"):
            url = url_for(".post", id=id)
        elif (type == "question"):
            url = url_for(".view_question", question_id=id)
        try:
            send_email_text(current_app.config["ADMIN_EMAIL"], "举报消息",
                            '用户({})举报({}),内容如下:\n{}'.format(user_url, url, form.body.data))
            flash("举报成功")
            return redirect(request.referrer or url_for('.index'))
        except smtplib.SMTPException:
            flash("举报失败")
            return redirect(request.referrer or url_for('.index'))
    else:
        return render_template("report.html", form=form, id=id, type=type)
