from django.contrib.auth.base_user import BaseUserManager


class UserManager(BaseUserManager):

    use_in_migrations = True

    def _create_user(self, username, email, password, **extra_fields):
        """
        Creates and saves a User with the given email and password.
        """

        if not email:
            raise ValueError('The given email must be set')
        email = self.normalize_email(email)
        username = self.get_by_natural_key(username)
        user = self.model(email=email, username=username, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_user(self, email,  matricule, last_name, password=None, **extra_fields):
        extra_fields.setdefault('is_superuser', False)
        #extra_fields.setdefault('username', matricule+"_"+last_name)
        username = matricule+"_"+last_name

        return self._create_user(username, email, password, **extra_fields)

    def create_superuser(self, email, matricule, last_name, password, **extra_fields):
        extra_fields.setdefault('is_superuser', True)
        #extra_fields.setdefault('username', matricule+"_"+last_name)
        username = matricule+"_"+last_name

        if extra_fields.get('is_superuser') is not True:
            raise ValueError('Superuser must have is_superuser=True.')

        return self._create_user(username, email, password, **extra_fields)
