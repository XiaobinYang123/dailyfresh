# Dailyfresh

- Language：Python2.* (Django)
- Databases: MySql、 redis
- Task Queue: celery(django-celery)
- File distributed System: FastDFS
- Search Engine: haystack(django-haystack)、whoosh
- web server: Nginx+ uwsgi

### Applications

------

- Products
- Users
- Orders
- Cart



## Optimization

Redis: save the SQL data for home page, sessionId, user history and static file

FastDFS: put the image to FastDFS and use Nginx to get the Image. This will decrease the server pressure.
