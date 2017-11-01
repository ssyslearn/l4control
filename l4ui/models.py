from django.db import models
from django.utils import timezone

class L4(models.Model):
    virtual_ip = models.CharField(max_length=200)
    svc_name = models.CharField(max_length=200)
    virtual_port = models.CharField(max_length=200)
    sticky = models.CharField(max_length=200)
    dsr = models.CharField(max_length=200)
    ssl_cert = models.CharField(max_length=200)
    real_server = models.CharField(max_length=200)
    real_ip = models.CharField(max_length=200)
    real_port = models.CharField(max_length=200)
    lb_mode = models.CharField(max_length=200)
    monitor = models.CharField(max_length=200)
    discription = models.TextField()
    created_date = models.DateTimeField(default=timezone.now)
    published_date = models.DateTimeField(blank=True, null=True)

    def publish(self):
        self.published_date = timezone.now()
        self.save()

    def __str__(self):
        return self.vip
