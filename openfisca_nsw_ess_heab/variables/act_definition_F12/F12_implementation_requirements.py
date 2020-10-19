# Import from openfisca-core the common Python objects used to code the legislation in OpenFisca
from openfisca_core.model_api import *
# Import the Entities specifically defined for this tax and benefit system
from openfisca_nsw_base.entities import *


class F12_steam_boiler_exhaust_temp_below_180C(Variable):
    value_type = bool
    entity = Building
    definition_period = ETERNITY
    label = 'If the End User Equipment is a steam boiler, is the exhaust' \
            ' temperature existing the End-User Equipment while at high-firing' \
            ' below 180C?'

    def formula(buildings, period, parameters):
        equipment_type = buildings('F12_existing_equipment_type', period)
        EquipmentType = equipment_type.possible_values
        is_steam_boiler = (equipment_type == EquipmentType.steam_boiler)
        exhaust_temperature = buildings('F12_exhaust_temperature', period)
        condition_temp_below_180C = (exhaust_temperature < 180)
        return ((is_steam_boiler * condition_temp_below_180C) +
                (not(is_steam_boiler)))


class F12_hot_water_or_heater_exhaust_temp_below_100C(Variable):
    value_type = bool
    entity = Building
    definition_period = ETERNITY
    label = 'If the End User Equipment is a steam boiler, is the exhaust' \
            ' temperature existing the End-User Equipment while at high-firing' \
            ' below 180C?'

    def formula(buildings, period, parameters):
        equipment_type = buildings('F12_existing_equipment_type', period)
        EquipmentType = equipment_type.possible_values
        is_condensing_steam_boiler = (equipment_type == EquipmentType.condensing_steam_boiler)
        is_hot_water_boiler = (equipment_type == EquipmentType.hot_water_boiler)
        is_water_heater = (equipment_type == EquipmentType.water_heater)
        exhaust_temperature = buildings('F12_exhaust_temperature', period)
        condition_temp_below_100C = (exhaust_temperature < 100)
        return ((is_condensing_steam_boiler + is_hot_water_boiler + is_water_heater)
                * condition_temp_below_100C +
                (not(is_condensing_steam_boiler)) * (not(is_hot_water_boiler)) * (not(is_water_heater)))


class F12_installed_in_accordance_with_manufacturer_guidelines(Variable):
    value_type = bool
    entity = Building
    definition_period = ETERNITY
    label = 'Is the equipment installed in accordance with manufacturer guidelines?'


class F12_installed_in_accordance_with_relevant_standards_and_legislation(Variable):
    value_type = bool
    entity = Building
    definition_period = ETERNITY
    label = 'Is the equipment installed in accordance with relevant standards' \
            ' and legislation?'


class F12_installed_in_accordance_with_scheme_administrator_requirements(Variable):
    value_type = bool
    entity = Building
    definition_period = ETERNITY
    label = 'Is the equipment installed in accordance with other Scheme' \
            ' Administrator Requirements?'


class F12_meets_implementation_requirements(Variable):
    value_type = bool
    entity = Building
    definition_period = ETERNITY
    label = 'Does the equipment meet the Equipment Requirements of Activity' \
            ' Definition F12?'

    def formula(buildings, period, parameters):
        steam_boiler_exhaust_temp_below_180C = buildings('F12_steam_boiler_exhaust_temp_below_180C', period)
        hot_water_boiler_or_heater_temp_below_100C = buildings('F12_hot_water_or_heater_exhaust_temp_below_100C', period)
        adheres_to_manufacturers_guidelines = buildings('F12_installed_in_accordance_with_manufacturer_guidelines', period)
        adheres_to_relevants_standards_and_legislation = buildings('F12_installed_in_accordance_with_relevant_standards_and_legislation', period)
        adheres_to_scheme_administrator_requirements = buildings('F12_installed_in_accordance_with_scheme_administrator_requirements', period)
        return ((steam_boiler_exhaust_temp_below_180C * hot_water_boiler_or_heater_temp_below_100C)
                * (adheres_to_manufacturers_guidelines * adheres_to_relevants_standards_and_legislation
                * adheres_to_scheme_administrator_requirements))
