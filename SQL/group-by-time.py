"""
Group by minute
Input:
    6	2020-12-09 09:29:04.215836
    7	2020-12-09 09:29:18.682882
    8	2020-12-09 09:29:19.831128
    9	2020-12-09 09:29:34.918914
    10	2020-12-09 09:29:37.036617
    11	2020-12-09 09:29:38.672620
    12	2020-12-09 09:29:40.311120
    13	2020-12-09 09:29:40.820016
    14	2020-12-09 09:29:41.537559
    15	2020-12-09 09:29:53.676690
    16	2020-12-09 09:30:02.336606
    17	2020-12-09 09:30:03.815859
    18	2020-12-09 09:30:05.412835
    19	2020-12-09 09:30:15.673348
    20	2020-12-09 09:34:50.976693
    21	2020-12-09 09:34:53.490987
Output:
    [
        {'log_minute': '17:29', 'log_count': 10},
        {'log_minute': '17:30', 'log_count': 4}, 
        {'log_minute': '17:34', 'log_count': 2}
    ]
"""

def format(x):
    return '%02d' % x

from datetime import datetime
from django.db.models import Count
from django.db.models.functions import Trunc

qs = Log.objects.all().annotate(log_minute=Trunc('created', 'minute')).values('log_minute').annotate(log_count=Count('id'))
data = []
for it in qs:
    data.append({
        'log_minute': format(it['log_minute'].hour) + ':' + format(it['log_minute'].minute),
        'log_count': it['log_count'],
    })
data.sort(key=lambda it: it['log_minute'])