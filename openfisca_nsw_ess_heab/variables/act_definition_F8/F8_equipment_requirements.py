# Import from openfisca-core the common Python objects used to code the legislation in OpenFisca
from openfisca_core.model_api import *
# Import the Entities specifically defined for this tax and benefit system
from openfisca_nsw_base.entities import *


class F8_replacement_end_user_equipment_is_single_gas_fired_steam_boiler(Variable):
    value_type = bool
    entity = Building
    definition_period = ETERNITY
    label = 'Is the replacement end user equipment a single gas fired steam boiler?'


class F8_replacement_end_user_equipment_is_multiple_gas_fired_steam_boilers(Variable):
    value_type = bool
    entity = Building
    definition_period = ETERNITY
    label = 'Is the replacement end user equipment multiple gas fired steam boilers?'


class F8_minimum_nameplate_capacity(Variable):
    value_type = bool
    entity = Building
    definition_period = ETERNITY
    label = 'Is the nameplate capacity of the replacement End User Equipment over 200kW?'

    def formula(buildings, period, parameters):
        nameplate_capacity = buildings('F8_replacement_equipment_nameplate_capacity', period)
        return nameplate_capacity > 200


class F8_has_linkageless_burner(Variable):
    value_type = bool
    entity = Building
    definition_period = ETERNITY
    label = 'If the replacement End User Equipment has a nameplate capacity of' \
            ' 1000kW or above, does it have a linkageless burner with a turn-down' \
            ' ratio of at least 4:1?'

    def formula(buildings, period, parameters):
        has_linkageless_burner = buildings('F8_replacement_equipment_has_linkageless_burner_minimum_4_1', period)
        nameplate_capacity = buildings('F8_replacement_equipment_nameplate_capacity', period)
        condition_nameplate_capacity_over_1000kW = (nameplate_capacity > 1000)
        over_1000kW_and_has_linkageless_burner = where(condition_nameplate_capacity_over_1000kW,
                                                       has_linkageless_burner,
                                                       True)
        # if the capacity is under 1000kW, it doesn't matter if it has a linkageless \
        # burner - this will always be true


class F8_has_linkageless_burner_and_oxygen_trim_system(Variable):
    value_type = bool
    entity = Building
    definition_period = ETERNITY
    label = 'If the replacement End User Equipment has a nameplate capacity of' \
            ' 1000kW or above, does it have a linkageless burner with a turn-down' \
            ' ratio of at least 4:1?'

    def formula(buildings, period, parameters):
        nameplate_capacity = buildings('F8_replacement_equipment_nameplate_capacity', period)
        condition_nameplate_capacity_over_2000kW = (nameplate_capacity > 2000)
        has_oxygen_trim_system = buildings('F8_replacement_equipment_has_oxygen_trim_system', period)
        has_linkageless_burner = buildings('F8_has_linkageless_burner', period)
        over_2000kW_and_has_trim_system = where(condition_nameplate_capacity_over_2000kW,
                                                has_oxygen_trim_system * has_linkageless_burner,
                                                True)
        # if the capacity is under 2000kW, it doesn't matter if it has an oxygen \
        # trim system - this will always be true


class fuel_to_fluid_efficiency_above_80_percent(Variable):
    value_type = bool
    entity = Building
    definition_period = ETERNITY
    label = 'Is the fuel to fluid efficiency of the replacement End User Equipment' \
            ' above 80 percent?'

    def formula(buildings, period, parameters):
        fuel_to_fluid_efficiency = buildings('fuel_to_fluid_efficiency_at_high_fire_conditions', period)
        return fuel_to_fluid_efficiency >= 80.0


class F8_meets_relevant_standards_and_legislation(Variable):
    value_type = bool
    entity = Building
    definition_period = ETERNITY
    label = 'Does the new End User Equipment meet any relevant standards and legislation?'
    # WHat does this mean? Define this.


class F8_meets_equipment_requirements(Variable):
    value_type = bool
    entity = Building
    definition_period = ETERNITY
    label = 'Does the equipment meet the Equipment Requirements of Activity' \
            ' Definition F7?'

    def formula(buildings, period, parameters):
        is_single_or_multiple_gas_fired_steam_boilers = (buildings('F8_replacement_end_user_equipment_is_single_gas_fired_steam_boiler', period)
        + buildings('F8_replacement_end_user_equipment_is_multiple_gas_fired_steam_boilers', period))
        has_minimum_nameplate_capacity = buildings('F8_minimum_nameplate_capacity', period)
        has_linkageless_burner = buildings('F8_has_linkageless_burner', period)
        has_oxygen_trim_system = buildings('F8_has_linkageless_burner_and_oxygen_trim_system', period)
        efficiency_above_80_percent = buildings('fuel_to_fluid_efficiency_above_80_percent', period)
        meets_relevant_standards_and_legislation = buildings('F8_meets_relevant_standards_and_legislation', period)
        return (is_single_or_multiple_gas_fired_steam_boilers * has_minimum_nameplate_capacity
                * has_linkageless_burner * has_oxygen_trim_system * efficiency_above_80_percent
                * meets_relevant_standards_and_legislation)
