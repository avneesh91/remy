import pulp
from pulp import LpVariable, LpMinimize, LpProblem, lpSum, LpBinary
from typing import List
from remy.domain.dtos.record_dto import RecordDTO
from remy.domain.constants import CONFIDENCE_LEVEL

class DefaultRevisionOptimizer:
    """
    Rules for making sure we revise topics:
        1. Anything learned on day 0 must be revised on day 1, day3, day 7, day 5, day 10 and day 15.
        2. Everything should be revised with a timespan of 20 days.
        3. This revision should not take more than 3 hours a day.
        4. On an average you a high confidence thing will take 30 mins to revise, medium confidence
           about an hour and low confidence thing will take 2 hours(the items that need to revised are labelled as low/medium/high confidence)

    """

    REVISION_SCHEDULE_LIST = [1,3,7,15]

    def __init__(self, service_locater):
        self.service_locater = service_locater
        self._model = LpProblem("Revision Optimization", LpMinimize)

    def get_estimated_revision_time(self, record_dto: RecordDTO):
        """
        Returns the amount of time in minutes it takes to revise a topic based
        on the confidence level
        """
        confidence_level = record_dto.confidence_level

        if confidence_level == CONFIDENCE_LEVEL.LOW:
            return 60
        elif confidence_level == CONFIDENCE_LEVEL.MEDIUM:
            return 30
        elif confidence_level == CONFIDENCE_LEVEL.HIGH:
            return 15

        return 15

    def _get_variable_day(self, variable_id):
        return int(variable_id.split('_')[1])

    def get_revision_days(self, record_dto):
        days_since_learned = record_dto.days_since_learned()
        curr_list = list(filter(lambda x: x >= 0, [ i - days_since_learned for i in DefaultRevisionOptimizer.REVISION_SCHEDULE_LIST]))
        return set(curr_list)

    def _get_variable_dict(self, record_dto_list: List[RecordDTO]):
        record_id_dict = {}

        for record_dto in record_dto_list:
            record_id_dict[record_dto.row_id] = []

            for i in range(1, 21):
                record_id_dict[record_dto.row_id].append(f'{record_dto.row_id}_{i}')

        return record_id_dict

    def load_model(self, record_dto_list: List[RecordDTO]):
        record_variables_dict = self._get_variable_dict(record_dto_list)

        total_revision_time_constraint_list = []

        day_variable_dict = {}

        for record_dto in record_dto_list:
            id_list = record_variables_dict.get(record_dto.row_id)
            revision_time_in_mins = self.get_estimated_revision_time(record_dto)
            revision_days = self.get_revision_days(record_dto)

            variable_list = []

            for i in id_list:
                curr_variable = LpVariable(i,cat=LpBinary)
                variable_list.append(curr_variable)
                variable_day = self._get_variable_day(i)

                if not day_variable_dict.get(variable_day):
                    day_variable_dict[variable_day] = []

                day_variable_dict[variable_day].append(curr_variable * revision_time_in_mins)

                if int(variable_day) in revision_days:
                    self._model += curr_variable == 1

            if len(revision_days) < 1:
                self._model += lpSum([revision_time_in_mins * i for i in variable_list]) == 1

        import ipdb;ipdb.set_trace()
        for day in day_variable_dict.keys():
            var_list = day_variable_dict.get(day)
            self._model += lpSum(var_list) <= 180

    def optimize(self):
        self._model.solve(pulp.PULP_CBC_CMD())
        for v in self._model.variables():
             print(v.name, "=", v.varValue
