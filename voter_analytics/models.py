
# File: models.py
# Name: Tanish Gurung
# BU Username: tanishg
# Description: Defines the Voter model and functions for
# importing voter records from a CSV file.
# Voter Analytics: Models for storing Newton voter records.

from django.db import models
import csv
from datetime import date
from pathlib import Path

class Voter(models.Model):
    """Represents a registered voter in Newton, Massachusetts."""

    last_name = models.CharField(max_length=50)
    first_name = models.CharField(max_length=50)

    street_number = models.CharField(max_length=10)
    street_name = models.CharField(max_length=100)
    apartment_number = models.CharField(max_length=20, blank=True)
    zip_code = models.CharField(max_length=10)

    date_of_birth = models.DateField()
    date_of_registration = models.DateField(null=True, blank=True)
    party_affiliation = models.CharField(max_length=2)
    precinct_number = models.CharField(max_length=10)
    v20state = models.BooleanField(default=False)
    v21town = models.BooleanField(default=False)
    v21primary = models.BooleanField(default=False)
    v22general = models.BooleanField(default=False)
    v23town = models.BooleanField(default=False)

    voter_score = models.IntegerField(default=0)

    def __str__(self):
        """Return the voter's full name."""
        return f"{self.first_name} {self.last_name}"

def clean_date(value):
    """Convert a valid ISO date or return None for an invalid date."""
    try:
        return date.fromisoformat(value)
    except (ValueError, TypeError):
        return None

def load_data():
    """Read the Newton voters CSV file and save records to the database."""
    filename = Path(__file__).resolve().parent / "newton_voters.csv"

    if Voter.objects.exists():
        print("Voters already loaded. Skipping import.")
        return

    voters = []

    with open(filename, encoding="utf-8-sig", newline="") as file:
        reader = csv.DictReader(file)

        for row in reader:
            voter = Voter(
                last_name=row["Last Name"],
                first_name=row["First Name"],
                street_number=row["Residential Address - Street Number"],
                street_name=row["Residential Address - Street Name"],
                apartment_number=row["Residential Address - Apartment Number"],
                zip_code=row["Residential Address - Zip Code"],
                date_of_birth=clean_date(row["Date of Birth"]),
                date_of_registration=clean_date(row["Date of Registration"]),
                party_affiliation=row["Party Affiliation"].strip(),
                precinct_number=row["Precinct Number"],
                v20state=row["v20state"] == "TRUE",
                v21town=row["v21town"] == "TRUE",
                v21primary=row["v21primary"] == "TRUE",
                v22general=row["v22general"] == "TRUE",
                v23town=row["v23town"] == "TRUE",
                voter_score=int(row["voter_score"]),
            )
            voters.append(voter)

    Voter.objects.bulk_create(voters, batch_size=1000)
    print(f"Imported {len(voters)} voters.")
