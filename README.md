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

### Start

------

1. open MySQL and Redis

2. Go to virtual environment and download the package

3. start Nginx

4. start FastDFS and celery

   ```shell
   sudo service fdfs_storaged start
   sudo service fdfs_trackerd start
   celery -A celery_tasks.tasks worker -l info
   ```

5.  start uwsgi

   ```shell
   uwsgi --ini uwsgi.ini
   ```

   
