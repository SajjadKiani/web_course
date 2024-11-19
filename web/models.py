from django.db import models



# User Model
class MyUser(models.Model):
    id = models.AutoField(primary_key=True)
    username = models.CharField(max_length=255, unique=True)
    email = models.EmailField(unique=True)
    password = models.CharField(max_length=255)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.username

# Movie Model
class Movie(models.Model):
    id = models.AutoField(primary_key=True)
    title = models.CharField(max_length=255)
    description = models.TextField()
    release_date = models.DateField()
    rating = models.FloatField()
    duration = models.IntegerField()  # Duration in minutes
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.title

# Genre Model
class Genre(models.Model):
    id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=255)

    def __str__(self):
        return self.name

# Pivot table between Genre and Movie
class GenreMovie(models.Model):
    genre = models.ForeignKey(Genre, on_delete=models.CASCADE)
    movie = models.ForeignKey(Movie, on_delete=models.CASCADE)

    def __str__(self):
        return f"{self.genre.name} - {self.movie.title}"

# Comment Model
class Comment(models.Model):
    id = models.AutoField(primary_key=True)
    content = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    user = models.ForeignKey(MyUser, on_delete=models.CASCADE)  # Relation with User
    movie = models.ForeignKey(Movie, on_delete=models.CASCADE)  # Relation with Movie

    def __str__(self):
        return f"Comment by {self.user.username} on {self.movie.title}"

# Trailer Model
class Trailer(models.Model):
    id = models.AutoField(primary_key=True)
    url = models.URLField()
    movie = models.ForeignKey(Movie, on_delete=models.CASCADE)  # Relation with Movie

    def __str__(self):
        return f"Trailer for {self.movie.title}"

# UserMovie Model
class UserMovie(models.Model):
    id = models.AutoField(primary_key=True)
    user = models.ForeignKey(MyUser, on_delete=models.CASCADE)  # Relation with User
    movie = models.ForeignKey(Movie, on_delete=models.CASCADE)  # Relation with Movie
    rating = models.FloatField()  # User's rating for the movie
    watched_status = models.BooleanField()  # Whether the user has watched the movie
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.user.username} - {self.movie.title} (Watched: {self.watched_status}, Rating: {self.rating})"


