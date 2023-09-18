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
  "open_conversations_about_differences": "people talk about their differences",
  "differences_in_major_and_sorority": "two different worlds within major and sorority",
  "racism_common_in_sorority": "people think racism is common in sorority",
  "discussions_about_racism_in_classes": "talking about realities of racism in classes",
  "need_to_seek_out_spaces": "need to seek out spaces to talk about race",
  "limited_spaces_for_race_discussions": "some spaces are not open to race discussions",
  "racial_consciousness_in_classes": "racial consciousness in Chicano Studies",
  "friendship_facilitates_dialogue": "friendship facilitates dialogue about difference",
  "ignorant_viewpoints_on_race": "encountering ignorant viewpoints on race",
  "uncomfortable_discussions_about_race": "uncomfortable discussions about race",
  "discussions_in_student_government": "discussions about race in student government",
  "facilitating_dialogue_with_empathy": "facilitating dialogue with empathy",
  "taboos_prevent_dialogue": "societal taboos prevent dialogue",
  "uncomfortable_talking_about_sexuality": "uncomfortable discussing sexuality with ex-girlfriend",
  "smaller_things_trigger_inhibition": "smaller things inhibit comfortable conversations",
  "conversations_in_dorms_and_jobs": "conversations in dorms and workplace",
  "comfortable_talking_about_differences": "comfortable talking about differences at work",
  "limited_connections_outside_dorm": "less connected to UCLA outside of dorm",
  "conversations_in_classes_and_clubs": "conversations in classes and clubs",
  "embarrassment_and_fear_prevent_dialogue": "embarrassment and fear prevent dialogue",
  "honesty_in_discussions_about_differences": "honesty in discussions about differences",
  "interactions_in_clubs_and_organizations": "interactions in clubs and organizations",
  "pride_in_sharing_culture": "pride in sharing Armenian culture"
}
"""

themes = """
{
    "themes": [
        {
            "theme": "Frequency of Conversations",
            "code": [
                "open_conversations_about_differences",
                "differences_in_major_and_sorority",
                "racism_common_in_sorority",
                "discussions_about_racism_in_classes",
                "need_to_seek_out_spaces",
                "limited_spaces_for_race_discussions",
                "racial_consciousness_in_classes",
                "friendship_facilitates_dialogue",
                "ignorant_viewpoints_on_race",
                "uncomfortable_discussions_about_race",
                "discussions_in_student_government",
                "facilitating_dialogue_with_empathy",
                "taboos_prevent_dialogue",
                "uncomfortable_talking_about_sexuality",
                "smaller_things_trigger_inhibition",
                "conversations_in_dorms_and_jobs",
                "comfortable_talking_about_differences",
                "limited_connections_outside_dorm",
                "conversations_in_classes_and_clubs",
                "embarrassment_and_fear_prevent_dialogue",
                "honesty_in_discussions_about_differences",
                "interactions_in_clubs_and_organizations",
                "pride_in_sharing_culture"
            ]
        },
        {
            "theme": "Context of Conversations",
            "code": [
                "differences_in_major_and_sorority",
                "racism_common_in_sorority",
                "discussions_about_racism_in_classes",
                "limited_spaces_for_race_discussions",
                "racial_consciousness_in_classes",
                "conversations_in_dorms_and_jobs",
                "limited_connections_outside_dorm",
                "conversations_in_classes_and_clubs",
                "interactions_in_clubs_and_organizations"
            ]
        },
        {
            "theme": "Desire for More Conversations",
            "code": [
                "need_to_seek_out_spaces",
                "discussions_in_student_government",
                "facilitating_dialogue_with_empathy",
                "taboos_prevent_dialogue",
                "embarrassment_and_fear_prevent_dialogue"
            ]
        },
        {
            "theme": "Depth of Conversations",
            "code": [
                "discussions_about_racism_in_classes",
                "racial_consciousness_in_classes",
                "facilitating_dialogue_with_empathy",
                "honesty_in_discussions_about_differences"
            ]
        },
        {
            "theme": "Improvement in Conversations",
            "code": [
                "uncomfortable_discussions_about_race",
                "taboos_prevent_dialogue",
                "embarrassment_and_fear_prevent_dialogue"
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
