from django.views.generic.edit import FormView
from django.contrib.auth.models import User
from django.core.urlresolvers import reverse_lazy
from django.db import transaction
from django.contrib.auth import login, authenticate
from accounts.forms import UserProfileForm
from accounts.forms import SignUpForm
from accounts.models import UserProfile

class SignUpView(FormView):
    template_name = 'accounts/signup.html'
    form_class = SignUpForm
    success_url = reverse_lazy('main:home')

    def get(self, request, *args, **kwargs):
        form = SignUpForm()
        profile_form = UserProfileForm()
        return self.render_to_response(self.get_context_data(form=form, profile_form=profile_form))

    def custom_form_invalid(self, form, profile_form):
        return self.render_to_response(self.get_context_data(form=form, profile_form=profile_form))

    def post(self, request, *args, **kwargs):
        form = self.get_form(self.get_form_class())
        profile_form = UserProfileForm(self.request.POST)
        if form.is_valid() and profile_form.is_valid():
            SignUpView.register_user(form.cleaned_data, profile_form.cleaned_data, self.request)
            return self.form_valid(form)
        else:
            return self.custom_form_invalid(form, profile_form)



    @classmethod
    @transaction.atomic
    def register_user(cls, form, pform, request):
        user = User.objects.create_user(username=form['username'],
                                        email=form['email'],
                                        password=form['password'],
                                        first_name=form['first_name'],
                                        last_name=form['last_name'])
        profile = UserProfile.objects.create(user=user,
                                             room_number=pform['room_number'],
                                             group_number=pform['group_number'],
                                             money=0,
                                             is_activated=False,
                                             mobile=pform['mobile'],
                                             middle_name=pform['middle_name'],
                                             hostel=pform['hostel'],
                                             status=pform['status'],
                                             sex=pform['sex'])
        user = authenticate(username=form['username'], password=form['password'])
        login(request, user)
        # make_log(request.user, u'Пользователь ' + request.user.get_full_name() + u' (' + request.user.username + u') только что зарегистрировался на сайте.')

