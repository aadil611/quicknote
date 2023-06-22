from django.db import models

class Note(models.Model):
    CONTENT_TYPE_CHOICES = (
        ('text', 'Text'),
        ('audio', 'Audio'),
        ('video', 'Video'),
    )
    
    title = models.CharField(max_length=128)
    content_type = models.CharField(max_length=8, choices=CONTENT_TYPE_CHOICES, default='text')
    owner = models.ForeignKey('auth.User', related_name='notes', on_delete=models.CASCADE)
    shared_with = models.ManyToManyField('auth.User', related_name='shared_notes', blank=True)
    text = models.TextField(blank=True)
    audio = models.FileField(upload_to='audio/', blank=True)
    video = models.FileField(upload_to='video/', blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)


    def __str__(self):
        return f'{self.title}'

    