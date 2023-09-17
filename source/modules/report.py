import json
import pandas as pd


summary = """
Based on the two transcripts, students have mixed perceptions of the quality and accessibility of food services on campus. While some aspects are appreciated, there is room for improvement. The affordability of food is a concern for students on a tight budget, as some options can be expensive. The variety and diversity of food options are generally decent, but students would like to see more international and culturally diverse choices.

Students have different dietary restrictions and preferences, such as being vegetarian or trying to eat healthy. The college does offer some accommodations, but there is a desire for more variety in vegetarian and healthy options.

In terms of dining choices, students find the weekly meal plan and pay-as-you-go options beneficial for managing their expenses and having flexibility in choosing when and what to eat. Some students also use food delivery services or order food from off-campus when they want specific cuisines not available on campus.

Student feedback does seem to have some impact on food services, with changes being made in response to requests for healthier options. However, some students feel that the college could be more responsive to their suggestions and make more improvements based on feedback.

There are some sustainability initiatives in place, such as recycling bins and compostable utensils, but students feel that more can be done to reduce waste and promote sustainability.

Overall, students have varying levels of satisfaction with the food services on campus. Factors such as affordability, variety, dietary accommodations, and responsiveness to feedback influence their perceptions and dining choices. Students would like to see improvements in vegetarian options, affordability, transparency in pricing, and regular updates on changes or improvements planned for the future.
"""

codes = """
{
    "experience_mixed": "overall experience mixed",
    "favorite_dishes": "favorite dishes chicken Alfredo pasta",
    "accommodate_restrictions": "college accommodate dietary restrictions",
    "affordability_challenging": "affordability of food challenging",
    "beneficial_meal_plan": "beneficial weekly meal plan",
    "variety_diversity_options": "variety and diversity of food options",
    "improvements_feedback": "improvements based on student feedback",
    "sustainability_initiatives": "sustainability initiatives recycling bins",
    "food_delivery_off_campus": "food delivery services off-campus",
    "improving_vegetarian_options": "recommendations improving vegetarian options",
    "experience_decent": "overall experience decent",
    "accommodate_healthy_options": "college accommodate healthy options",
    "affordability_mixed_bag": "affordability of food mixed bag",
    "beneficial_pay_as_you_go": "beneficial pay-as-you-go option",
    "broader_range_healthy_options": "recommendations broader range healthy options"
}
"""

themes = """
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
            # Search for code in keys of json1_data
            if c in json1_data.keys():
                excerpts_combined.append(json1_data[c])
        excerpts_combined = set(excerpts_combined)
        cleaned_data_dict["Excerpts from transcript"].append(", ".join(excerpts_combined))

    return pd.DataFrame(cleaned_data_dict)
