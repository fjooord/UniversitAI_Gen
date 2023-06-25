import requests
import json
import Utils.Chat_GPT_Funcs as GPT
from PIL import Image
from io import BytesIO
import matplotlib.pyplot as plt

ELAI_API = "gvGKAhdmh1OiEcZ2KY3qZIciRA90dOL7"

class VideoTemplate:
    def __init__(self, template_id, slide_templates=None):
        self.template_id = template_id
        self.slide_templates = slide_templates if slide_templates is not None else []

    def add_slide_template(self, slide_template):
        self.slide_templates.append(slide_template)

    def remove_slide_template(self, slide_template):
        if slide_template in self.slide_templates:
            self.slide_templates.remove(slide_template)

    def __str__(self):
        return f"VideoTemplate(id={self.template_id}, slides={self.slide_templates})"

class SlideTemplate:
    def __init__(self, slide_template_id, hasHeader=False, hasSubheader=False, hasList=False, hasImage=False):
        self.slide_template_id = slide_template_id
        self.hasHeader = hasHeader
        self.hasSubheader = hasSubheader
        self.hasList = hasList
        self.hasImage = hasImage

    def __str__(self):
        return f"SlideTemplate(id={self.slide_template_id}, hasHeader={self.hasHeader}, hasSubheader={self.hasSubheader}, hasList={self.hasList}, hasImage={self.hasImage})"


def make_empty_story(template_id):
    """
    Function creates an empty story with the given template id
    This will be filled in later with a PATCH command
    """
    url = "https://apis.elai.io/api/v1/story/text"

    payload = {
        "templateId": f"{template_id}",
        "from": ""
    }
    headers = {
        "accept": "application/json",
        "content-type": "application/json",
        "Authorization": f"Bearer {ELAI_API}"
    }

    response = requests.post(url, json=payload, headers=headers)

    print(response.text)
    return response.text