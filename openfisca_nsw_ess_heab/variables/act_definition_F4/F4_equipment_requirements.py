# Import from openfisca-core the common Python objects used to code the legislation in OpenFisca
from openfisca_core.model_api import *
# Import the Entities specifically defined for this tax and benefit system
from openfisca_nsw_base.entities import *


class EUE_is_registered_in_GEMS(Variable):
    value_type = bool
    entity = Building
    definition_period = ETERNITY
    label = 'Asks whether the End User Equipment is registered under GEMS.'  # you could theoretically have a list of all of the products and ask the user to input their product - and then if it's not in the list, fail this.


class complies_with_GEMS_determination(Variable):
    value_type = bool
    entity = Building
    definition_period = ETERNITY
    label = 'Asks whether the EUE complies with the Greenhouse and Energy' \
            ' Minimum Standards (Air Conditioners up to 65kW) Determination 2019.'  # figure out what it means to be compliant and then input those are


class AEER_is_20_percent_greater_than_baseline(Variable):
    value_type = bool
    entity = Building
    definition_period = ETERNITY
    label = 'asks whether the AEER of the relevant AC is at least 20 percent' \
            ' greater than the Baseline Cooling AEER, as required in' \
            ' Equipment Requirement 2 of Activity Definition F4.'


class ACOP_is_20_percent_greater_than_baseline(Variable):
    value_type = bool
    entity = Building
    definition_period = ETERNITY
    label = 'asks whether the ACOP of the relevant AC is at least 20 percent' \
            ' greater than the Baseline Heating ACOP, as required in' \
            ' Equipment Requirement 2 of Activity Definition F4.'


class AEER(Variable):
    value_type = float
    entity = Building
    definition_period = ETERNITY
    label = 'returns the AEER for the relevant product, as defined in GEMS' \
            ' (Air Conditioners up to 65kW) Determination.'

    def formula(buildings, period, parameters):
        cooling_capacity = buildings('cooling_capacity', period)
        power_input = buildings('power_input', period)
        Pia = buildings('weighted_average_inactive_power_consumption', period)
        return (cooling_capacity / 2000) / (power_input * 2000) + (Pia * 6.76)


class ACOP(Variable):
    value_type = float
    entity = Building
    definition_period = ETERNITY
    label = 'returns the ACOP for the relevant product, as defined in GEMS' \
            ' (Air Conditioners up to 65kW) Determination.'

    def formula(buildings, period, parameters):
        heating_capacity = buildings('heating_capacity', period)
        power_input = buildings('power_input', period)
        Pia = buildings('weighted_average_inactive_power_consumption', period)
        return (heating_capacity / 2000) / (power_input * 2000) + (Pia * 6.76)


class cooling_capacity_is_eligible(Variable):
    value_type = bool
    entity = Building
    definition_period = ETERNITY
    label = 'Asks whether the user input cooling capacity is less than 65kW' \
            ' as required by Equipment Requirement 4 of Activity Definition F4.'

    def formula(buildings, period, parameters):
        cooling_capacity = buildings('cooling_capacity', period)
        return cooling_capacity < 65


class heating_capacity_is_eligible(Variable):
    value_type = bool
    entity = Building
    definition_period = ETERNITY
    label = 'Asks whether the user input heating capacity is less than 65kW' \
            ' as required by Equipment Requirement 4 of Activity Definition F4.'

    def formula(buildings, period, parameters):
        heating_capacity = buildings('heating_capacity', period)
        return heating_capacity < 65


class cooling_capacity(Variable):
    value_type = float
    entity = Building
    definition_period = ETERNITY
    label = 'Asks for the cooling capacity of the relevant AC in kW.'


class heating_capacity(Variable):
    value_type = float
    entity = Building
    definition_period = ETERNITY
    label = 'Asks for the heating capacity of the relevant AC in kW.'


class power_input(Variable):
    value_type = float
    entity = Building
    definition_period = ETERNITY
    label = 'Asks for the power input of the relevant AC in kW.'


class weighted_average_inactive_power_consumption(Variable):
    value_type = float
    entity = Building
    definition_period = ETERNITY
    label = 'Asks for the Weighted Average Inactive Power Consumption of the' \
            ' relevant AC, measured in W, as defined in AS 3823.4.1:2014.'  # note, sourced from EnergyAE report. need to double source this formula.

    def formula(buildings, period, parameters):
        power_inactive_mode_at_5C = buildings('inactive_power_measured_at_5C', period)
        power_inactive_mode_at_10C = buildings('inactive_power_measured_at_10C', period)
        power_inactive_mode_at_15C = buildings('inactive_power_measured_at_15C', period)
        power_inactive_mode_at_20C = buildings('inactive_power_measured_at_20C', period)
        return (0.05 * power_inactive_mode_at_5C
                + 0.13 * power_inactive_mode_at_10C
                + 0.27 * power_inactive_mode_at_15C
                + 0.55 * power_inactive_mode_at_20C)


class inactive_power_measured_at_5C(Variable):
    value_type = float
    entity = Building
    definition_period = ETERNITY
    label = 'Returns the power measured in inactive mode, in W, at 5 degrees' \
            ' Celsius.'  # please check the unit


class inactive_power_measured_at_10C(Variable):
    value_type = float
    entity = Building
    definition_period = ETERNITY
    label = 'Returns the power measured in inactive mode, in W, at 10 degrees' \
            ' Celsius.'  # please check the unit


class inactive_power_measured_at_15C(Variable):
    value_type = float
    entity = Building
    definition_period = ETERNITY
    label = 'Returns the power measured in inactive mode, in W, at 15 degrees' \
            ' Celsius.'  # please check the unit


class inactive_power_measured_at_20C(Variable):
    value_type = float
    entity = Building
    definition_period = ETERNITY
    label = 'Returns the power measured in inactive mode, in W, at 20 degrees' \
            ' Celsius.'  # please check the unit
