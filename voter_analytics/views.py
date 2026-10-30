
# File: views.py
# Name: Tanish Gurung
# BU Username: tanishg
# Description: Defines views for displaying and filtering
# voter records in the Voter Analytics application.

from datetime import date

from django.views.generic import ListView, DetailView
from .models import Voter
import plotly.graph_objects as go
from django.db.models import Count
from django.db.models.functions import ExtractYear


class VoterListView(ListView):
    """Display and filter a paginated list of voters."""

    model = Voter
    template_name = "voter_analytics/voters.html"
    context_object_name = "voters"
    paginate_by = 100
    ordering = ["last_name", "first_name"]

    def get_queryset(self):
        """Return voters matching the selected GET filters."""
        voters = super().get_queryset()

        party = self.request.GET.get("party", "")
        min_year = self.request.GET.get("min_year", "")
        max_year = self.request.GET.get("max_year", "")
        voter_score = self.request.GET.get("voter_score", "")

        if party:
            voters = voters.filter(party_affiliation=party)

        if min_year:
            voters = voters.filter(date_of_birth__year__gte=int(min_year))

        if max_year:
            voters = voters.filter(date_of_birth__year__lte=int(max_year))

        if voter_score:
            voters = voters.filter(voter_score=int(voter_score))

        elections = [
            "v20state",
            "v21town",
            "v21primary",
            "v22general",
            "v23town",
        ]

        for election in elections:
            if self.request.GET.get(election):
                voters = voters.filter(**{election: True})

        return voters

    def get_context_data(self, **kwargs):
        """Add filter choices and selected values to the template context."""
        context = super().get_context_data(**kwargs)

        context["parties"] = (
            Voter.objects.order_by("party_affiliation")
            .values_list("party_affiliation", flat=True)
            .distinct()
        )

        context["years"] = range(1900, date.today().year + 1)
        context["scores"] = range(6)
        context["selected"] = self.request.GET

        params = self.request.GET.copy()
        params.pop("page", None)
        context["query_string"] = params.urlencode()

        return context


class VoterDetailView(DetailView):
    """Display all information for an individual voter."""

    model = Voter
    template_name = "voter_analytics/voter_detail.html"
    context_object_name = "voter"


class VoterGraphsView(VoterListView):
    """Display aggregate graphs of voter data using selected filters."""

    template_name = "voter_analytics/graphs.html"
    paginate_by = None

    def get_context_data(self, **kwargs):
        """Create three graphs using the filtered voter records."""
        context = super().get_context_data(**kwargs)
        voters = self.get_queryset()

        # Graph 1: Distribution of voters by birth year
        birth_years = (
            voters.annotate(year=ExtractYear("date_of_birth"))
            .values("year")
            .annotate(total=Count("id"))
            .order_by("year")
        )

        fig1 = go.Figure(data=[
            go.Bar(
                x=[item["year"] for item in birth_years],
                y=[item["total"] for item in birth_years],
            )
        ])
        fig1.update_layout(
            title="Voters by Birth Year",
            xaxis_title="Birth Year",
            yaxis_title="Number of Voters",
        )

        # Graph 2: Distribution by party affiliation
        parties = (
            voters.values("party_affiliation")
            .annotate(total=Count("id"))
            .order_by("party_affiliation")
        )

        fig2 = go.Figure(data=[
            go.Pie(
                labels=[p["party_affiliation"] for p in parties],
                values=[p["total"] for p in parties],
            )
        ])
        fig2.update_layout(title="Voters by Party Affiliation")

        # Graph 3: Participation in past elections
        elections = [
            "v20state", "v21town", "v21primary",
            "v22general", "v23town"
        ]

        counts = [
            voters.filter(**{election: True}).count()
            for election in elections
        ]

        fig3 = go.Figure(data=[
            go.Bar(
                x=["2020 State", "2021 Town", "2021 Primary",
                   "2022 General", "2023 Town"],
                y=counts,
            )
        ])
        fig3.update_layout(
            title="Election Participation",
            xaxis_title="Election",
            yaxis_title="Number of Voters",
        )

        context["graph1"] = fig1.to_html(
            full_html=False, include_plotlyjs="cdn"
        )
        context["graph2"] = fig2.to_html(
            full_html=False, include_plotlyjs=False
        )
        context["graph3"] = fig3.to_html(
            full_html=False, include_plotlyjs=False
        )

        return context

