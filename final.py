from flask import Flask, request
from flask_sqlalchemy import SQLAlchemy
from flask_marshmallow import Marshmallow
from flask_restful import Api, Resource

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///new.db'
db = SQLAlchemy(app)
ma = Marshmallow(app)
api = Api(app)

class Post(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(50))
    occupation = db.Column(db.String(255))

    def __repr__(self):
        return '<Post %s>' % self.name

class PostSchema(ma.Schema):
    class Meta:
        fields = ("id", "name", "occupation")
        model = Post

class PostListResource(Resource):
    def get(self):
        posts = Post.query.all()
        return posts_schema.dump(posts)
    def post(self):
        new_post = Post(
            name=request.json['name'],
            occupation=request.json['occupation']
        )
        db.session.add(new_post)
        db.session.commit()
        return post_schema.dump(new_post)

class PostResource(Resource):
    def get(self, post_id):
        post = Post.query.get_or_404(post_id)
        return post_schema.dump(post)
    def patch(self, post_id):
        post = Post.query.get_or_404(post_id)

        if 'name' in request.json:
            post.name = request.json['name']
        if 'occupation' in request.json:
            post.content = request.json['content']

        db.session.commit()
        return post_schema.dump(post)

    def delete(self, post_id):
        post = Post.query.get_or_404(post_id)
        db.session.delete(post)
        db.session.commit()
        return '', 204

api.add_resource(PostResource, '/posts/<int:post_id>')
api.add_resource(PostListResource, '/posts')

post_schema = PostSchema()
posts_schema = PostSchema(many=True)





if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0')

