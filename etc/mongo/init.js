conn = new Mongo();
db = conn.getDB('ugc_movies');

db.createCollection('likes');
db.createCollection('bookmarks');
db.createCollection('reviews');
