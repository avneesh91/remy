import questionary
from rich.console import Console
from remy.io.handlers import BaseHandler
from remy.domain.service_locater import ServiceLocater
from remy.domain.constants import ENTITY_IDENTIFIERS, CONFIDENCE_LEVEL
from remy.domain.helpers import topic_name_validator
from remy.domain.dtos.record_dto import RecordDTO

class RecordAdditionHandler(BaseHandler):
    ADD_NEW = 'Add New'

    def __init__(self, service_locater: ServiceLocater):
        self.service_locater = service_locater
        self.storage = service_locater.misc_mapping.get(ENTITY_IDENTIFIERS.LOCAL_STORAGE)
        self.console = Console()

    def get_all_topics(self):
        return self.storage.get_all_topics()

    def run_input_prompt(self):
       topic_choices = self.get_all_topics() + [RecordAdditionHandler.ADD_NEW]
       new_topic = False
       new_category = False

       choice = questionary.autocomplete(
            "Please  a topic that you'd like to add an item about",
            choices=topic_choices
        ).ask()

        if choice == RecordAdditionHandler.ADD_NEW:
            topic_name = questionary.text("Topic Name:", validate=topic_name_validator).ask()
            self.storage.add_topic(topic_name)
            choice = topic_name
            new_topic = True

        dto = RecordDTO.get_new_record_dto(choice)

        if new_topic == True:
            category_choice = questionary.text('Category:').ask()
        else:
            category_choices = self.storage.get_categories(choice) + [RecordAdditionHandler.ADD_NEW]

            category_choice = questionary.autocomplete(
                "Please choose category",
                choices= category_choices).ask()

            if category_choice == RecordAdditionHandler.ADD_NEW:
                 category_choice = questionary.text("Category:").ask()
                 new_category = True

        dto.category = category_choice

        if new_category == True:
            sub_category_choice = questionary.text('Sub-Category:').ask()
        else:
            sub_category_choices = self.storage.get_subcategories(choice, category_choice) + [RecordAdditionHandler.ADD_NEW]

            sub_category_choice = questionary.autocomplete(
                'Please  sub category',
                choices=sub_category_choices
            ).ask()

            if sub_category_choice == RecordAdditionHandler.ADD_NEW:
                sub_category_choice =  questionary.text('Sub-Category:').ask()

        dto.sub_category = sub_category_choice

        dto.notes = questionary.text("Add notes").ask()

        dto.confidence_level = questionary.(
            "What is you confidence level in this topic?"
            choices=CONFIDENCE_LEVEL.get_confidence_choices())

        confirm_addition = questionary.confirm("Confirm Addition?").ask()

        table = dto.get_record_table_for_print()
        self.console(table)

        questionary.print("Add this info? 🦄", style="bold fg:green")


        if confirm_addition:
            self.storage.add_record(dto)



    def run(self):
        pass
