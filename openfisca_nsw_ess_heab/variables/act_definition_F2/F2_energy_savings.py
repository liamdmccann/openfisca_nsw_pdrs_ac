# Import from openfisca-core the common Python objects used to code the legislation in OpenFisca
from openfisca_core.model_api import *
# Import the Entities specifically defined for this tax and benefit system
from openfisca_nsw_base.entities import *


class F2_electricity_savings(Variable):
    value_type = float
    entity = Building
    definition_period = ETERNITY
    label = 'What is the electricity savings for the activity conducted within' \
            ' Activity Definition F2?'

    def formula(buildings, period, parameters):
        IPLV = buildings('F2_integrated_part_load_value', period)
        cooling_capacity = buildings('F2_cooling_capacity', period)
        LCP_type = buildings('F2_LCP_type', period)
        capacity = select([cooling_capacity >= 350 and cooling_capacity <= 499,
                           cooling_capacity >= 500 and cooling_capacity <= 699,
                           cooling_capacity >= 700 and cooling_capacity <= 999,
                           cooling_capacity >= 1000 and cooling_capacity <= 1499,
                           cooling_capacity > 1500],
                          ['350_to_499_kWR',
                           '500_to_699_kWR',
                           '700_to_999_kWR',
                           '1000_to_1499_kWR',
                           'greater_than_1500_kWR'])
        baseline = parameters(period).HEAB.F2.F2_1[LCP_type][capacity]
        EFLH = parameters(period).HEAB.F2.equivalent_full_load_hours
        lifetime = parameters(period).HEAB.F2.lifetime
        MWh_conversion = parameters(period).general_ESS.MWh_conversion
        energy_savings = ((((cooling_capacity / baseline) - (cooling_capacity / IPLV))
                         * EFLH * lifetime) / MWh_conversion)
        return energy_savings


class F2LCPType(Enum):
    air_cooled = 'Product is an air-cooled LCP.'
    water_cooled = 'Product is a water-cooled LCP.'


class F2_LCP_type(Variable):
    value_type = Enum
    possible_values = F2LCPType
    default_value = F2LCPType.air_cooled
    entity = Building
    definition_period = ETERNITY
    label = 'What is the product type for the new liquid chilled package End' \
            ' User Equipment?'


class F2_integrated_part_load_value(Variable):
    value_type = float
    entity = Building
    definition_period = ETERNITY
    label = 'What is the integrated part load value for the new Liquid' \
            ' Chilling Package, as determined using AS 4776?'


class F2_cooling_capacity(Variable):
    value_type = float
    entity = Building
    definition_period = ETERNITY
    label = 'What is the total rated cooling capacity for the new Liquid' \
            ' Chilling Package, as determined using AS 4776?'
