### install
```
pip install celery
```
### define task
@celery.task
### run the celery worker
celery -A your_application.celery worker -l info
```
# bp_vchat is python file which celery is defined
celery -A main_app.bp_vchat worker -l info
```
