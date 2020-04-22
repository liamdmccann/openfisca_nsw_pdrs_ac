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


class ACOP(Variable):
    value_type = float
    entity = Building
    definition_period = ETERNITY
    label = 'returns the ACOP for the relevant product, as defined in GEMS' \
            ' (Air Conditioners up to 65kW) Determination.'


class cooling_capacity_is_eligible(Variable):
    value_type = bool
    entity = Building
    definition_period = ETERNITY
    label = 'Asks whether the user input cooling capacity is less than 65kW' \
            ' as required by Equipment Requirement 4 of Activity Definition F4.'

    def formula (buildings, period, parameters):
        cooling_capacity = buildings('cooling_capacity', period)
        return cooling_capacity < 65


class heating_capacity_is_eligible(Variable):
    value_type = bool
    entity = Building
    definition_period = ETERNITY
    label = 'Asks whether the user input heating capacity is less than 65kW' \
            ' as required by Equipment Requirement 4 of Activity Definition F4.'

    def formula (buildings, period, parameters):
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
