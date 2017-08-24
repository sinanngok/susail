from django import forms
from localflavor.tr.forms import TRPhoneNumberField
from .models import User

class UserCreationForm(forms.ModelForm):
    """A form for creating new users. Includes all the required
    fields, plus a repeated password."""
    phone_number = TRPhoneNumberField()

    class Meta:
        model = User
        fields = ('su_id', 'email', 'first_name', 'last_name', 'phone_number')

    def save(self, commit=True):
        # Save the provided password in hashed format
        user = super(UserCreationForm, self).save(commit=False)
        user.set_password(self.cleaned_data["password1"])
        if commit:
            user.save()
        return user

class UserChangeForm(forms.ModelForm):
    """A form for updating users. Includes all the fields on
    the user, but replaces the password field with admin's
    password hash display field.
    """
    password = ReadOnlyPasswordHashField()

    class Meta:
        model = User
        fields = (
            'first_name',
            'last_name',
            'email',
            'password',
            'date_of_birth',
            'is_active',
            #'is_staff',
            'emergency_contact_name',
            'emergency_phone_number',
            'sailing_level',
            'is_visible_on_web',
            'extra_information_about_member',
            'is_an_active_student',
            'is_school_staff',
            'is_gorbon_captain',
            'is_active_member',
            'club_management_position',
            'sailing_team_position',
            'susail_balance',
            'is_admin',
        )

    def clean_password(self):
        # Regardless of what the user provides, return the initial value.
        # This is done here, rather than on the field, because the
        # field does not have access to the initial value
        return self.initial["password"]