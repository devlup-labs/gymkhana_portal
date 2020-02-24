from django.utils import timezone
from django.views.generic import TemplateView, DetailView, ListView, CreateView
from .models import Society, Club, Senate, Activity, Contact
from festivals.models import Festival
from oauth.models import UserProfile
from .forms import ContactForm
from .mixins import NavigationMixin
from photologue.models import Gallery
from events.models import Event
from news.models import News
from .utils import MaintenanceMixin
from decouple import config


class MaintenanceAndNavigationMixin(MaintenanceMixin, NavigationMixin):
    pass


class HomeView(MaintenanceAndNavigationMixin, TemplateView):
    template_name = 'main/index.html'

    def get_context_data(self, **kwargs):
        context = super(HomeView, self).get_context_data(**kwargs)
        carousel = Gallery.objects.filter(title='HomePageCarousel').filter(is_public=True).first()
        events = Event.objects.filter(club=None)[:5]
        news = News.objects.filter(club=None)[:5]
        festivals = Festival.objects.all()
        gallery = Gallery.objects.filter(title='Home Page Gallery').filter(is_public=True).first()
        context['carousel'] = carousel
        context['event_list'] = events
        context['news_list'] = news
        context['festival_list'] = festivals
        context['gallery'] = gallery
        return context


class SocietyView(MaintenanceAndNavigationMixin, DetailView):
    template_name = 'main/society.html'
    model = Society

    def get_context_data(self, **kwargs):
        context = super(SocietyView, self).get_context_data(**kwargs)
        raw = self.object.club_set.filter(published=True)
        clubs = raw.filter(ctype='C')
        teams = raw.filter(ctype='T')
        events = Event.objects.filter(club__society=self.object).filter(published=True).filter(
            date__gte=timezone.now())[:5]
        news = News.objects.filter(club__society=self.object)[:5]
        context['club_list'] = clubs
        context['team_list'] = teams
        context['event_list'] = events
        context['news_list'] = news
        return context


class SenateView(MaintenanceAndNavigationMixin, DetailView):
    template_name = 'main/senate.html'
    model = Senate

    def get_context_data(self, **kwargs):
        context = super(SenateView, self).get_context_data(**kwargs)
        return context


class ClubView(MaintenanceAndNavigationMixin, DetailView):
    template_name = 'main/club.html'
    model = Club

    def get_context_data(self, **kwargs):
        context = super(ClubView, self).get_context_data(**kwargs)
        events = Event.objects.filter(club=self.object).filter(published=True).filter(date__gte=timezone.now())[:5]
        activities = Activity.objects.filter(club=self.object)
        news = News.objects.filter(club=self.object)[:5]
        members = self.object.core_members.all()
        context['event_list'] = events
        context['activity_list'] = activities
        context['news_list'] = news
        context['member_list'] = members
        return context


class ContactView(MaintenanceAndNavigationMixin, CreateView):
    template_name = 'main/contact.html'
    form_class = ContactForm


class ContactListView(MaintenanceAndNavigationMixin, ListView):
    template_name = 'main/contact_list.html'
    model = Contact
    paginate_by = 2

    def get_context_data(self, **kwargs):
        context = super(ContactListView, self).get_context_data(**kwargs)
        context['range'] = range(context["paginator"].num_pages)
        return context


class OfficeView(MaintenanceAndNavigationMixin, TemplateView):
    template_name = 'main/office.html'

    def get_context_data(self, **kwargs):
        context = super(OfficeView, self).get_context_data(**kwargs)
        secretary_roll_no = config('GENERAL_SECRETARY_ROLL', cast=str, default='')
        current_year = str(timezone.now().year)
        context.update({
            'general_secretary': UserProfile.objects.filter(
                roll=secretary_roll_no).first() if UserProfile.objects.filter(
                roll=secretary_roll_no).exists() else None,
            'societies': Society.objects.filter(year=current_year),
            'senate_secretary': Senate.objects.filter(year=current_year).first().senatemembership_set.filter(
                role='SECY').first().userprofile if Senate.objects.filter(
                year=current_year).exists() else None
        })
        return context
