from django.contrib import admin
from .models import MyUser, Movie, UserMovie, Genre, GenreMovie, Comment, Trailer

# Inline Admin for User's Favorite Movies
class UserMovieInline(admin.TabularInline):
    model = UserMovie
    extra = 0
    fields = ('movie', 'rating', 'watched_status', 'created_at')
    readonly_fields = ('created_at',)
    can_delete = True

# User Admin
@admin.register(MyUser)
class UserAdmin(admin.ModelAdmin):
    list_display = ('id', 'username', 'email', 'created_at')
    search_fields = ('username', 'email')
    inlines = [UserMovieInline]

# UserMovie Admin for Managing Favorites
@admin.register(UserMovie)
class UserMovieAdmin(admin.ModelAdmin):
    list_display = ('user', 'movie', 'rating', 'watched_status', 'created_at')
    search_fields = ('user__username', 'movie__title')
    list_filter = ('rating', 'created_at', 'watched_status')
    autocomplete_fields = ('user', 'movie')

    # Custom Action: Add a Movie to User's Favorites
    def add_movie_to_favorites(self, request, queryset):
        # Placeholder for the implementation
        self.message_user(request, "Feature to add movies manually will be added here.")
    add_movie_to_favorites.short_description = "Add a Movie to a User's Favorites"

    actions = ['add_movie_to_favorites']

class CommentInline(admin.TabularInline):
    model = Comment
    extra = 0
    fields = ('user', 'content', 'created_at')
    readonly_fields = ('created_at',)
    can_delete = True

# Inline Admin for GenreMovie
class GenreMovieInline(admin.TabularInline):
    model = GenreMovie
    extra = 1  # Number of empty rows to display for adding genres
    autocomplete_fields = ('genre',)  # Autocomplete for selecting genres
    can_delete = True  # Allow deletion of genres from the movie


@admin.register(Movie)
class MovieAdmin(admin.ModelAdmin):
    list_display = ('id', 'title', 'release_date', 'rating', 'duration')
    search_fields = ('title',)
    list_filter = ('release_date', 'rating')
    inlines = [CommentInline, GenreMovieInline]  # Display comments inline in the movie admin

class MovieFilter(admin.SimpleListFilter):
    title = 'Movie'
    parameter_name = 'movie'

    def lookups(self, request, model_admin):
        movies = Movie.objects.all()
        return [(movie.id, movie.title) for movie in movies]

    def queryset(self, request, queryset):
        if self.value():
            return queryset.filter(movie_id=self.value())
        return queryset

@admin.register(Comment)
class CommentAdmin(admin.ModelAdmin):
    list_display = ('id', 'movie', 'user', 'content', 'created_at')
    search_fields = ('user__username', 'movie__title', 'content')
    list_filter = ('created_at', MovieFilter)  # Add movie filter
    autocomplete_fields = ('movie', 'user')
    actions = ['delete_selected']

    # Enable filtering comments for a specific movie
    def get_queryset(self, request):
        qs = super().get_queryset(request)
        # Add custom queryset logic if needed
        return qs

    # Add custom action to delete selected comments
    def delete_selected(self, request, queryset):
        count = queryset.count()
        queryset.delete()
        self.message_user(request, f"{count} comment(s) deleted successfully.")
    delete_selected.short_description = "Delete Selected Comments"

# Trailer Admin
@admin.register(Trailer)
class TrailerAdmin(admin.ModelAdmin):
    list_display = ('id', 'movie', 'url')
    search_fields = ('movie__title',)
    autocomplete_fields = ('movie',)

# Genre Admin
@admin.register(Genre)
class GenreAdmin(admin.ModelAdmin):
    list_display = ('id', 'name')
    search_fields = ('name',)

# GenreMovie Admin
@admin.register(GenreMovie)
class GenreMovieAdmin(admin.ModelAdmin):
    list_display = ('genre', 'movie')
    autocomplete_fields = ('genre', 'movie')

