# TrackSpot

## Git
### Fixing the Database
When your branch says your database has changed but you know that you haven't changed it, do the following:
1. Delete your local database file `db.sqlite3`
2. Download the latest master database from [here](https://github.com/jswny/trackspot/raw/master/db.sqlite3)
3. Put this file back into your directory where you deleted the old one
4. Commit this and push if necessary

Then, when you go on your branch on GitHub and click the "compare" button below the "clone or download" button, it should **NOT** show that your database has changes.

## Users, Critics, & Groups
### Structure
- The previous `User` and `Critic` models have been removed, along with any of the existing entities which were in the database.
- Now, each "user" of either type is represented by a single `User` model using the built-in Django authentication user model
- Each of these models has an associated `Profile` model, which contains the extra information such as location and bio
- The `Profile` model has an optional `organization` field, which should be restricted so that it is always blank for Trackspotters but available to critics

### Getting the Current User
If you need to access the current user in a view or a template, you can access it with `request.user`, or `{{ user }}` in a template (since the `request` object is automatically loaded into the view for use).

To check if the user is logged in, use `request.user.is_authenticated()` in a view or something like `{% if user.is_authenticated() %}` in a template.

### Checking the Type for a Given User
To identify which kind of user the user that you have is (Trackspotter or Critic), you simply have to access the groups which are associated with that user model. To do this, you can use something like the following query:
```python
u = User.objects.get(username='john_doe')
groups = u.groups.values_list()
```
`u.groups.values_list()` will return a Django [QuerySet](https://docs.djangoproject.com/en/2.0/ref/models/querysets/) of which each entry is a tuple of `(group_id, group_name)` like `(1, 'Trackspotters')`. If you want to get just the name of a specific group, you can do something like `u.groups.values_list()[0][1]`, which will return the name (the second entry in the tuuple) of the first tuple from the queryset.

### Querying Groups
To get either kind of groups, do one of the following:
* `Group.objects.get(name='Trackspotters')`
* `Group.objects.get(name='Critics')`

## Querying Reviews for Albums or Songs
In order to find all critic and trackspotter (normal user) reviews for a given album, you can do something like this:
```python
critics = Group.objects.get(name='Critics')
trackspotters = Group.objects.get(name='Trackspotters')

album = Album.objects.get(id=1)

critic_reviews = Review.objects.filter(album__id=album.id).filter(user__groups=trackspotters)
trackspotter_reviews = Review.objects.filter(album__id=album.id).filter(user__groups=critics)
```

You can also get both kinds of reviews for a song similarly:
```python
critics = Group.objects.get(name='Critics')
trackspotters = Group.objects.get(name='Trackspotters')

song = Song.objects.get(id=1)

critic_reviews = Review.objects.filter(song__id=song.id).filter(user__groups=trackspotters)
trackspotter_reviews = Review.objects.filter(song__id=song.id).filter(user__groups=critics)
```

### Querying Profile Data
Querying the profile data for a given user (the parent Django auth model) is simple:
```python
u = User.objects.get(username='john_doe')
user_name = u.profile.name
user_bio = u.profile.bio
```

### Groups
The Django authentication system lets us define groups. We use these to differentiate between normal users and critics.
The following groups are defined:
* `Trackspotters` -- normal site users (non-critics), should not be able to access or modify the `organization` field of the `Profile` model
* `Critics` -- critics, who should be allowed to belong to and fill in the `organization` field of the `Profile` model

### Existing Users
| Username | Password | Type |
| -------- | -------- | ---- |
| `john_doe` | `compsci326` | Trackspotter |
| `bob_smith` | `compsci326` | Trackspotter |
| `fantano` | `compsci326` | Critic |
| `mason` | `compsci326` | Critic |