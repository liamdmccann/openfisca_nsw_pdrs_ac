# Import from openfisca-core the common Python objects used to code the legislation in OpenFisca
from openfisca_core.model_api import *
# Import the Entities specifically defined for this tax and benefit system
from openfisca_nsw_base.entities import *


class F10_gas_savings(Variable):
    value_type = float
    entity = Building
    definition_period = ETERNITY
    label = 'What is the electricity savings for the activity conducted within' \
            ' Activity Definition F10?'

    def formula(buildings, period, parameters):
        current_capacity = buildings('F10_current_equipment_capacity', period)
        existing_equipment_type = buildings('F10_existing_equipment_type', period)
        default_efficiency_improvement = parameters(period).HEAB.F10.table_F10_1.default_efficiency_improvement[existing_equipment_type]
        load_utilisation_factor = parameters(period).HEAB.F10.table_F10_2.load_utilisation_factor
        lifetime = parameters(period).HEAB.F10.table_F10_3.lifetime
        hours_in_year = parameters(period).general_ESS.hours_in_year
        MWh_conversion = parameters(period).general_ESS.unit_conversion_factors['kWh_to_MWh']
        return (current_capacity * default_efficiency_improvement * load_utilisation_factor
                * lifetime * hours_in_year / MWh_conversion)


class F10_current_equipment_capacity(Variable):
    value_type = float
    entity = Building
    definition_period = ETERNITY
    label = 'What is the nameplate capacity for the existing equipment, in kW?'


class F10EquipmentType(Enum):
    steam_boiler = 'Trim system is installed on a steam boiler.'
    hot_water_boiler = 'Trim system is installed on a hot water boiler.'
    water_heater = 'Trim system is installed on a water heater.'


class F10_existing_equipment_type(Variable):
    value_type = Enum
    possible_values = F10EquipmentType
    default_value = F10EquipmentType.steam_boiler
    entity = Building
    definition_period = ETERNITY
    label = 'What is the type of existing equipment that the trim system is being installed on?'
