import os
from pathlib import Path

FRESHNESS_DICT = {
    'Day':1,
    'Week':7,
    'Month':30,

}

REPORT_ONE_FORMAT_INSTRUCTIONS = """The output should be formatted as a JSON instance that conforms to the JSON schema below.

As an example, for the schema {{"properties": {{"foo": {{"title": "Foo", "description": "a list of strings", "type": "array", "items": {{"type": "string"}}}}}}, "required": ["foo"]}}
the object {{"foo": ["bar", "baz"]}} is a well-formatted instance of the schema. The object {{"properties": {{"foo": ["bar", "baz"]}}}} is not well-formatted.

Here is the output schema:
```
{{{
    "$defs": {{
        "report_demo": {{
            "properties": {{
                "new_title": {{
                    "description": "Title of the news article, Note do not use " character inside the string ",
                    "title": "New Title",
                    "type": "string"
                }},
                "relevance_to_triggers": {{
                    "description": "Explanation how the news is relevant/not relevant to triggers or not",
                    "title": "Relevance To Triggers",
                    "type": "string"
                }},
                "relevance_to_seller_offerings": {{
                    "description": "Explanation on how news artical is relevant/not relevant to the seller offerings ",
                    "title": "Relevance To Seller Offerings",
                    "type": "string"
                }},
                "source": {{
                    "description": "URL of the article",
                    "title": "Source",
                    "type": "string"
                }},
                "campaign_worthy": {{
                    "description": "if the news is campaign worthy or not",
                    "title": "Campaign Worthy",
                    "type": "boolean"
                }},
                "relevance_score": {{
                    "description": " relevance score of the news artical in the scale of [1-10]",
                    "title": "Relevance Score",
                    "type": "integer"
                }},
                "date": {{
                    "description": "Article Date",
                    "title": "Date",
                    "type": "string"
                }},
                "article_id": {{
                    "description": "Article id",
                    "title": "Article Id",
                    "type": "string"
                }},
                "action_items": {{
                    "description": "List of campaign ideas",
                    "items": {{
                        "type": "string"
                    }},
                    "title": "Action Items",
                    "type": "array"
                }}
            }},
            "required": [
                "new_title",
                "relevance_to_triggers",
                "relevance_to_seller_offerings",
                "source",
                "campaign_worthy",
                "relevance_score",
                "date",
                "action_items",
                "article_id"
            ],
            "title": "report_demo",
            "type": "object"
        }}
    }},
    "properties": {{
        "articles_report": {{
            "description": "Report of all the news articles",
            "items": {{
                "$ref": "#/$defs/report_demo"
            }},
            "title": "Articles Report",
            "type": "array"
        }}
    }},
    "required": [
        "articles_report"
    ]
}}
```"""


SESSION_SORT_NEWS_BY_KEY = "sort_by"
BASE_DIR = Path(__file__).resolve().parent.parent


TEMP_BASE_JSON_DIR = os.path.join(BASE_DIR,"news_collection_comparison/temp/json")
TEMP_BASE_REPORT_DIR = "temp/reports/"
READ_REPORT_BASE_DIR = os.path.join(BASE_DIR,"news-poc")
AYLIEN_LANG_OPETION = ["en", "de", "fr", "it", "es", "pt"]
# AYLIEN_LANG_OPETION
# AYLIEN_LANG_OPETION
# AYLIEN_LANG_OPETION
# AYLIEN_LANG_OPETION



