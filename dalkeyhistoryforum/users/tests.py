from django.test import TestCase
from django.contrib.auth.models import User
from django.core.files.uploadedfile import SimpleUploadedFile
from .forms import UserRegisterForm, UserUpdateForm, ProfileUpdateForm
from .models import Profile

class UserFormsTests(TestCase):

    def setUp(self):
        self.user = User.objects.create_user(username='testuser', password='12345')
        Profile.objects.get_or_create(user=self.user, defaults={'image': 'default.png'})

    def test_user_register_form(self):
        form_data = {
            'username': 'newuser',
            'email': 'newuser@fake.com',
            'password1': 'testing1234',
            'password2': 'testing1234'
        }
        form = UserRegisterForm(data=form_data)
        self.assertTrue(form.is_valid())

    def test_user_update_form(self):
         form_data = {
            'username': 'updateduser',
            'email': 'updateuser@fake.com',
        }
         form = UserUpdateForm(data=form_data, instance=self.user)
         self.assertTrue(form.is_valid())
         form.save()
         self.user.refresh_from_db()
         self.assertEqual(self.user.username, 'updateduser')

    def test_profile_update_with_invalid_image_format(self):
        invalid_image_data = b'this is not real image data'
        invalid_image_file = SimpleUploadedFile('new_image.txt', invalid_image_data, content_type='text/plain')
        form = ProfileUpdateForm(files={'image': invalid_image_file}, instance=self.user.profile)
        self.assertFalse(form.is_valid())

    def test_profile_update_with_oversized_image(self):
        oversized_image_data = b'\x00' * 10485760 
        oversized_image_file = SimpleUploadedFile('new_image.jpg', oversized_image_data, content_type='image/jpeg')
        form = ProfileUpdateForm(files={'image': oversized_image_file}, instance=self.user.profile)
        self.assertFalse(form.is_valid())
