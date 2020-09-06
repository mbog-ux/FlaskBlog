from flask import Blueprint,flash,redirect,render_template,request,url_for
from flaskblog import db
from flaskblog.posts.forms import PostForm
from flaskblog.models import User,Post
from flask_login import current_user,login_required

posts = Blueprint('posts',__name__)

@posts.route('/post/new',methods=['GET','POST'])
@login_required
def new_post():
    form = PostForm()
    if form.validate_on_submit():
        post = Post(title=form.title.data,content=form.content.data,author=current_user)
        db.session.add(post)
        db.session.commit()
        flash('Post has been posted','success')
        return redirect(url_for('main.home'))
    return render_template('create_post.html',form=form,legend='New Post',title='New Post')


@posts.route('/post/<int:post_id>')
def post(post_id):
    post = Post.query.get_or_404(int(post_id))
    return render_template('post.html',post=post,legend='Post')

@posts.route('/post/<int:post_id>/update',methods=['GET','POST'])
@login_required
def update_post(post_id):
    post = Post.query.get_or_404(int(post_id))
    if current_user != post.author:
        abort(403)
    form = PostForm()
    if form.validate_on_submit():
        post.title=form.title.data
        post.content = form.content.data
        db.session.commit()
        flash('Your post has been updated!','success')
        return redirect(url_for('posts.post',post_id=post.id))
    elif request.method == 'GET':
        form.title.data = post.title
        form.content.data = post.content

    return render_template('create_post.html',form=form,legend='Update Post')

@posts.route('/post/<int:post_id>/delete',methods=['POST'])
@login_required
def delete_post(post_id):
    post = Post.query.get_or_404(int(post_id))
    if current_user != post.author:
        abort(403)
    db.session.delete(post)
    db.session.commit()
    flash('Your post has been deleted!', 'success')
    return redirect(url_for('main.home'))


@posts.route('/post/<string:username>')
def user_posts(username):
    page = request.args.get('page',default=1,type=int)
    user = User.query.filter_by(username=username).first_or_404()
    posts = Post.query.order_by(Post.date_posted.desc()).filter_by(author=user).paginate(page=page,per_page=5)
    return render_template('user_posts.html',user=user,posts=posts)