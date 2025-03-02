import os
from celery import Celery
from django.conf import settings
import logging.config

# Django settings module을 설정합니다.
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.settings.local')

app = Celery('estimate_project')

# 로깅 설정
app.conf.update(
    task_track_started=True,
    task_serializer='json',
    accept_content=['json'],
    result_serializer='json',
    timezone='Asia/Seoul',
    enable_utc=False,
    worker_redirect_stdouts=False,
    worker_redirect_stdouts_level='INFO',
)

# Django의 settings 모듈을 Celery 설정으로 사용합니다.
app.config_from_object('django.conf:settings', namespace='CELERY')

# Django 앱 내의 tasks.py 파일에서 태스크를 자동으로 로드합니다.
app.autodiscover_tasks()

# 워커 수 설정 (옵션)
#app.conf.worker_concurrency = int(os.environ.get('CELERY_WORKER_CONCURRENCY', 10))

# 프리페치 수 설정 (옵션)
app.conf.worker_prefetch_multiplier = int(os.environ.get('CELERY_WORKER_PREFETCH_MULTIPLIER', 1))

# 추가 설정
app.conf.task_acks_late = True
app.conf.task_reject_on_worker_lost = True

# 태스크 기본 재시도 설정
app.conf.task_default_retry_delay = 1 * 5  # 5초 간격으로 재시도
app.conf.task_annotations = {'*': {'max_retries': 0}}

#app.conf.worker_pool = 'gevent'

# 로깅 설정
logging.config.dictConfig({
    'version': 1,
    'disable_existing_loggers': False,
    'formatters': {
        'verbose': {
            'format': '%(asctime)s [%(levelname)s] [%(processName)s] [%(name)s] %(message)s'
        },
    },
    'handlers': {
        'console': {
            'class': 'logging.StreamHandler',
            'formatter': 'verbose'
        },
    },
    'loggers': {
        'celery': {
            'handlers': ['console'],
            'level': 'INFO',
        },
        'tasks': {
            'handlers': ['console'],
            'level': 'DEBUG',
        }
    }
})
