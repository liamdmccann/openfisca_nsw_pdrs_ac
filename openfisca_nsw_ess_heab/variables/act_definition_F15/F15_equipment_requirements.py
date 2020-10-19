# Import from openfisca-core the common Python objects used to code the legislation in OpenFisca
from openfisca_core.model_api import *
# Import the Entities specifically defined for this tax and benefit system
from openfisca_nsw_base.entities import *


class F15_end_user_equipment_is_residual_blowdown_heat_exchanger(Variable):
    value_type = bool
    entity = Building
    definition_period = ETERNITY
    label = 'Is the equipment installed a residual blowdown heat exchanger?'


class F15_end_user_equipment_heat_transfer_temperature_less_than_40C(Variable):
    value_type = bool
    entity = Building
    definition_period = ETERNITY
    label = 'Is the temperature of the heat transfer, from the steam boiler\'s' \
            ' blowdown fluid, to a fluid stream, less than 40C?'


class F15_meets_equipment_requirements(Variable):
    value_type = bool
    entity = Building
    definition_period = ETERNITY
    label = 'Does the equipment meet the Equipment Requirements of Activity' \
            ' Definition F15?'

    def formula(buildings, period, parameters):
        equipment_is_blowdown_heat_exchanger = buildings('F15_end_user_equipment_is_residual_blowdown_heat_exchanger', period)
        heat_transfer_less_than_40C = buildings('F15_end_user_equipment_heat_transfer_temperature_less_than_40C', period)
        return(equipment_is_blowdown_heat_exchanger * heat_transfer_less_than_40C)
