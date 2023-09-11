import re
from typing import List
from pydantic import BaseModel, Field, validator

from langchain.output_parsers import PydanticOutputParser


class ExcerptCode(BaseModel):
    excerpt: str = Field(description="Relevant excerpt from the transcript")
    code: str = Field(description="Code generated that best represent the excerpts identified")

    @validator("code")
    def code_is_not_long(cls, info):
        size_code = len(re.split(r',|-|_|/| ', info))
        if size_code < 2 or size_code > 5:
            raise ValueError("Each code must be between two to five words long."
                             f"The code {info} is {size_code} long.")
        return info


class ExcerptCodes(BaseModel):
    excerpt_code: List[ExcerptCode] = Field(description="List of excerpt and code generated")


class Theme(BaseModel):
    theme: str = Field(description="Theme that was identified")
    code: List[str] = Field(description="List of codes categorized by theme identified")


class Themes(BaseModel):
    themes: List[Theme] = Field(description="List of themes identified")

    @validator("themes")
    def themes_is_not_long(cls, info):
        size_list_themes = len(info)
        if size_list_themes > 6:
            raise ValueError("The number of themes must not exceed 6."
                             f"{size_list_themes} over 6 was generated.")
        return info


code_parser = PydanticOutputParser(pydantic_object=ExcerptCodes)
theme_parser = PydanticOutputParser(pydantic_object=Themes)
