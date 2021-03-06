from django import forms
from django.db.models import Q
from django.forms import ModelForm, Select, TextInput
from django.forms.models import formset_factory
from issf_admin.models import UserProfile
from issf_base.models import Country, ISSF_Core, SelectedAttribute, SelectedThemeIssue, DidYouKnow, FAQ, WhoFeature, SSFPerson, SSFKnowledge


class SearchForm(forms.Form):
    """
    Form for searching for records.
    """
    fulltext_keywords = forms.CharField(
        label='Search by full text',
        required=False,
        widget=TextInput(attrs={'placeholder': 'Search'})
    )
    keywords = forms.CharField(label='Search by title', required=False)

    # contributor_id=1 is the ISSF Staff account
    existing_contributors = ISSF_Core.objects.all().values('contributor')
    contributor_choices = [
        (u.id, '%s (%s %s %s)' % (u.username, u.first_name, u.initials, u.last_name)) for u in UserProfile.objects.filter(
            Q(id__in=existing_contributors)
        ).order_by('username')
    ]
    contributor_choices.insert(0, ('', '------------------'))
    contributor = forms.ChoiceField(
        choices=contributor_choices,
        label='Contributor/editor',
        required=False
    )
    contribution_begin_date = forms.IntegerField(label='Contribution year begin', required=False)
    contribution_end_date = forms.IntegerField(label='Contribution year end', required=False)
    countries = forms.MultipleChoiceField(
        choices=[(c.country_id, c.short_name) for c in Country.objects.order_by('short_name')] + [("", "")],
        required=False
    )


class SelectedAttributeForm(ModelForm):
    """
    Form for searching for selected attributes.
    Not used on it's own, rather used as a part of a formset.
    """
    class Meta:
        fields = '__all__'
        model = SelectedAttribute
        widgets = {'attribute_value': Select}


class SelectedThemeIssueForm(ModelForm):
    """
    Form for searching for selected themes/issues.
    Not used on it's own, rather used as a part of a formset.
    """
    class Meta:
        model = SelectedThemeIssue
        fields = '__all__'
        # widgets = {'theme_issue_value': Select}


class TipForm(ModelForm):
    """
    Form for submitting new tips.
    """
    fact = forms.CharField()

    class Meta:
        model = DidYouKnow
        fields = '__all__'


class FAQForm(ModelForm):
    """
    Form for submitting new FAQ entries.
    """

    class Meta:
        model = FAQ
        fields = '__all__'


class WhosWhoForm(ModelForm):
    """
    Form for changing the who feature on the front page.
    """
    name = forms.CharField()
    about = forms.CharField(required=False)

    def __init__(self, *args, **kwargs) -> None:
        super(WhosWhoForm, self).__init__(*args, **kwargs)
        self.fields['ssf_person'].queryset = SSFPerson.objects.all().order_by(
            'contributor__last_name',
            'contributor__first_name'
        )
        self.fields['ssf_knowledge'].queryset = SSFKnowledge.objects.all().order_by('level2_title', 'level1_title')

    class Meta:
        model = WhoFeature
        fields = '__all__'
        labels = {
            'ssf_person': 'Who\'s Who Page',
            'ssf_knowledge': 'Select Publication'
        }
        widgets = {
            'ssf_knowledge': Select(attrs={'id': 'sota-select'}),
            'ssf_person': Select(attrs={'id': 'who-select'})
        }


class GeoJSONUploadForm(forms.Form):
    """
    Form for uploading a new GeoJSON file.
    """
    file = forms.FileField(required=False)


SelectedAttributesFormSet = formset_factory(SelectedAttributeForm, extra=1)
SelectedThemesIssuesFormSet = formset_factory(SelectedThemeIssueForm, extra=6)
