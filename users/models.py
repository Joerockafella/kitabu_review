import io
from io import BytesIO
from django.db import models
from django.contrib.auth.models import User
from django.core.files.storage import default_storage as s3_storage
from PIL import Image


class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    image = models.ImageField(default="default.jpg", upload_to="profile_pics")

    def __str__(self):
        return f"{self.user.username} Profile"

    # To resize the profile image once uploaded for AWS
    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)

        img_s3_read = s3_storage.open(self.image.name, "r")
        img = Image.open(img_s3_read)

        if img.height > 300 or img.width > 300:
            output_size = (300, 300)
            img.thumbnail(output_size)
            in_mem_file = io.BytesIO()
            img.save(in_mem_file, format="PNG")
            img_s3 = s3_storage.open(self.image.name, "w+")
            img_s3.write(in_mem_file.getvalue())
            img_s3.close()

        img_s3_read.close()

