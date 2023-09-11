import json
import pandas as pd
import streamlit as st

summary="""
Based on the two transcripts, students have mixed perceptions of the quality and accessibility of food services on campus. While some aspects are appreciated, there is room for improvement. The affordability of food is a concern for students on a tight budget, as some options can be expensive. The variety and diversity of food options are generally decent, but students would like to see more international and culturally diverse choices.

Students have different dietary restrictions and preferences, such as being vegetarian or trying to eat healthy. The college does offer some accommodations, but there is a desire for more variety in vegetarian and healthy options.

In terms of dining choices, students find the weekly meal plan and pay-as-you-go options beneficial for managing their expenses and having flexibility in choosing when and what to eat. Some students also use food delivery services or order food from off-campus when they want specific cuisines not available on campus.

Student feedback does seem to have some impact on food services, with changes being made in response to requests for healthier options. However, some students feel that the college could be more responsive to their suggestions and make more improvements based on feedback.

There are some sustainability initiatives in place, such as recycling bins and compostable utensils, but students feel that more can be done to reduce waste and promote sustainability.

Overall, students have varying levels of satisfaction with the food services on campus. Factors such as affordability, variety, dietary accommodations, and responsiveness to feedback influence their perceptions and dining choices. Students would like to see improvements in vegetarian options, affordability, transparency in pricing, and regular updates on changes or improvements planned for the future.
"""


codes="""
[
  {"excerpt": "overall experience mixed", "code": "experience_mixed"},
  {"excerpt": "favorite dishes chicken Alfredo pasta", "code": "favorite_dishes"},
  {"excerpt": "college accommodate dietary restrictions", "code": "accommodate_restrictions"},
  {"excerpt": "affordability of food challenging", "code": "affordability_challenging"},
  {"excerpt": "beneficial weekly meal plan", "code": "beneficial_meal_plan"},
  {"excerpt": "variety and diversity of food options", "code": "variety_diversity_options"},
  {"excerpt": "improvements based on student feedback", "code": "improvements_feedback"},
  {"excerpt": "sustainability initiatives recycling bins", "code": "sustainability_initiatives"},
  {"excerpt": "food delivery services off-campus", "code": "food_delivery_off_campus"},
  {"excerpt": "recommendations improving vegetarian options", "code": "improving_vegetarian_options"},
  {"excerpt": "overall experience decent", "code": "experience_decent"},
  {"excerpt": "favorite dishes classic cheeseburger", "code": "favorite_dishes"},
  {"excerpt": "college accommodate healthy options", "code": "accommodate_healthy_options"},
  {"excerpt": "affordability of food mixed bag", "code": "affordability_mixed_bag"},
  {"excerpt": "beneficial pay-as-you-go option", "code": "beneficial_pay_as_you_go"},
  {"excerpt": "variety and diversity of food options", "code": "variety_diversity_options"},
  {"excerpt": "improvements based on student feedback", "code": "improvements_feedback"},
  {"excerpt": "sustainability initiatives reusable trays", "code": "sustainability_initiatives"},
  {"excerpt": "food delivery services off-campus", "code": "food_delivery_off_campus"},
  {"excerpt": "recommendations broader range healthy options", "code": "broader_range_healthy_options"}
]
"""

themes="""
{
  "themes": [
    {
      "theme": "Mixed Perceptions",
      "code": [
        "experience_mixed",
        "experience_decent"
      ]
    },
    {
      "theme": "Affordability Concerns",
      "code": [
        "affordability_challenging",
        "affordability_mixed_bag"
      ]
    },
    {
      "theme": "Variety and Diversity",
      "code": [
        "variety_diversity_options",
        "variety_diversity_options"
      ]
    },
    {
      "theme": "Dietary Accommodations",
      "code": [
        "accommodate_restrictions",
        "accommodate_healthy_options"
      ]
    },
    {
      "theme": "Dining Choices",
      "code": [
        "beneficial_meal_plan",
        "beneficial_pay_as_you_go"
      ]
    },
    {
      "theme": "Feedback and Improvements",
      "code": [
        "improvements_feedback",
        "improvements_feedback"
      ]
    },
    {
      "theme": "Sustainability Initiatives",
      "code": [
        "sustainability_initiatives",
        "sustainability_initiatives"
      ]
    },
    {
      "theme": "Off-Campus Options",
      "code": [
        "food_delivery_off_campus",
        "food_delivery_off_campus"
      ]
    },
    {
      "theme": "Vegetarian Options",
      "code": [
        "improving_vegetarian_options",
        "broader_range_healthy_options"
      ]
    }
  ]
}
"""


def _clean_themes_data(themes):
    # Create an empty set to store unique codes
    unique_codes = set()

    # Create a new list to store themes with unique codes
    themes_with_unique_codes = []

    # Iterate through the themes and remove duplicates
    for theme_data in themes["themes"]:
        theme = theme_data["theme"]
        codes = theme_data["code"]

        # Replace underscores with spaces and filter out duplicates
        cleaned_codes = list(set([code.replace("_", " ") for code in codes]))

        # Filter out duplicates and add only unique codes to the set
        unique_codes.update(cleaned_codes)

        # Create a new theme entry with unique codes
        theme_entry = {
            "theme": theme,
            "code": list(set(cleaned_codes))  # Convert the list to a set to remove duplicates
        }
        themes_with_unique_codes.append(theme_entry)

    # Update the JSON data with themes containing unique codes
    themes["themes"] = themes_with_unique_codes
    return themes


def _clean_codes_data(codes):
    return list({"excerpt": code["excerpt"],
                 "code": code["code"].replace("_", " ")} for code in codes)


def parse_codes(_codes, _themes):
    # Create an empty dictionary to store the cleaned data
    cleaned_data_dict = {"Theme": [], "Codes": [], "Excerpts from transcript": []}

    # Create a set to store unique codes
    json1_data = json.loads(_codes)
    json2_data = json.loads(_themes)

    # Fill columns
    for theme_data in json2_data["themes"]:
        theme = theme_data["theme"]
        codes = set(theme_data["code"])  # Remove duplicates
        code = ", ".join([d.replace("_", " ") for d in codes])  # Replace underscores with spaces
        cleaned_data_dict["Theme"].append(theme)
        cleaned_data_dict["Codes"].append(code)
        excerpts_combined = []
        for c in codes:
            for item in json1_data:
                if c == item["code"]:
                    excerpts_combined.append(item["excerpt"])
        excerpts_combined = set(excerpts_combined)
        cleaned_data_dict["Excerpts from transcript"].append(", ".join(excerpts_combined))

    return pd.DataFrame(cleaned_data_dict)
