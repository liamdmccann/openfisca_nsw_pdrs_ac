# Import from openfisca-core the common Python objects used to code the legislation in OpenFisca
from openfisca_core.model_api import *
# Import the Entities specifically defined for this tax and benefit system
from openfisca_nsw_base.entities import *


class F5_is_electronically_communtated_motor(Variable):
    value_type = bool
    entity = Building
    definition_period = ETERNITY
    label = 'Is the product an electronically communtated (brushless DC) motor?'


class F5_nominal_input_power_less_than_500W(Variable):
    value_type = bool
    entity = Building
    definition_period = ETERNITY
    label = 'Is the nominal input power of the new End User Equipment less than' \
            ' or equal to 500W?'

    def formula(buildings, period, parameters):
        equipment_input_power = buildings('motor_nominal_input_power', period)
        condition_less_than_500W = (equipment_input_power <= 500)
        return condition_less_than_500W


class output_power_greater_than_existing_fan(Variable):
    value_type = bool
    entity = Building
    definition_period = ETERNITY
    label = 'Is the output power of the new equipment equal or greater than the' \
            ' existing equipment?'

    def formula(buildings, period, parameters):
        existing_output_power = buildings('existing_equipment_output_power', period)
        new_output_power = buildings('new_equipment_output_power', period)
        condition_new_power_higher_than_existing = (new_output_power >= existing_output_power)
        return condition_new_power_higher_than_existing


class airflow_volume_greater_than_existing_fan(Variable):
    value_type = bool
    entity = Building
    definition_period = ETERNITY
    label = 'Is the airflow volume of the new equipment equal or greater than the' \
            ' existing equipment?'

    def formula(buildings, period, parameters):
        existing_airflow_volume = buildings('existing_equipment_airflow_volume', period)
        new_airflow_volume = buildings('new_equipment_airflow_volume', period)
        condition_new_airflow_volume_higher_than_existing = (new_airflow_volume >= existing_airflow_volume)
        return condition_new_airflow_volume_higher_than_existing


class output_power_or_airflow_greater_than_existing_fan(Variable):
    value_type = bool
    entity = Building
    definition_period = ETERNITY
    label = 'Is the output power or the airflow volume of the new equipment' \
            ' equal or greater than the existing equipment?'

    def formula(buildings, period, parameters):
        output_power_greater = buildings('output_power_greater_than_existing_fan', period)
        airflow_greater = buildings('airflow_volume_greater_than_existing_fan', period)
        return output_power_greater + airflow_greater


class meets_other_scheme_administrator_requirements(Variable):
    value_type = bool
    entity = Building
    definition_period = ETERNITY
    label = 'Does the product meet any other requirements specified by the' \
            ' Scheme Administrator, including the suitability of the impeller' \
            ' for the motor?'
    # what does complying with this Determination mean?


class F5_meets_equipment_requirements(Variable):
    value_type = bool
    entity = Building
    definition_period = ETERNITY
    label = 'Does the equipment meet the Equipment Requirements of Activity' \
            ' Definition F4?'

    def formula(buildings, period, parameters):
        is_electronically_communtated_motor = buildings('F5_is_electronically_communtated_motor', period)
        input_less_than_500W = buildings('F5_nominal_input_power_less_than_500W', period)
        higher_output_or_airflow = buildings('output_power_or_airflow_greater_than_existing_fan', period)
        meets_other_requirements = buildings('meets_other_scheme_administrator_requirements', period)
        return (is_electronically_communtated_motor * input_less_than_500W
        * higher_output_or_airflow * meets_other_requirements)
