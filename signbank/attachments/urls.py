from django.conf.urls import *
from signbank.attachments.views import *

urlpatterns = [
    
    url(r'^$', AttachmentListView.as_view(), name="attachments"),
    url(r'^upload/', upload_file),
]

