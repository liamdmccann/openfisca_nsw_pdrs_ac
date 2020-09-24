# Import from openfisca-core the common Python objects used to code the legislation in OpenFisca
from openfisca_core.model_api import *
# Import the Entities specifically defined for this tax and benefit system
from openfisca_nsw_base.entities import *


class F4_electricity_savings(Variable):
    value_type = float
    entity = Building
    definition_period = ETERNITY
    label = 'What is the electricity savings for the activity conducted within' \
            ' Activity Definition F4?'

    def formula(buildings, period, parameters):
        reference_cooling_annual_energy_use = buildings('F4_reference_cooling_annual_energy_use', period)
        cooling_annual_energy_use = buildings('F4_cooling_annual_energy_use', period)
        reference_heating_annual_energy_use = buildings('F4_reference_heating_annual_energy_use', period)
        heating_annual_energy_use = buildings('F4_heating_annual_energy_use', period)
        lifetime = parameters(period).HEAB.F4.lifetime
        MWh_conversion = parameters(period).general_ESS.MWh_conversion
        return (((reference_cooling_annual_energy_use - cooling_annual_energy_use)
        + (reference_heating_annual_energy_use - heating_annual_energy_use)) * lifetime / MWh_conversion)


class F4_reference_cooling_annual_energy_use(Variable):
    value_type = float
    entity = Building
    definition_period = ETERNITY
    label = 'What is the reference cooling annual energy use for the AC, as' \
            ' defined in Table F4.4?'

    def formula(buildings, period, parameters):
        cooling_capacity = buildings('cooling_capacity', period)
        weather_zone = buildings('weather_zone', period)
        cooling_hours = parameters(period).HEAB.F4.cooling_and_heating_hours.cooling_hours[weather_zone]
        product_class = buildings('F4_product_class', period)
        baseline_cooling_AEER = parameters(period).HEAB.F4.baseline_AEER_and_ACOP.AEER[product_class]
        return cooling_capacity * cooling_hours / baseline_cooling_AEER


class cooling_capacity(Variable):
    value_type = float
    entity = Building
    definition_period = ETERNITY
    label = 'What is the cooling capacity for Activity Definition F4?'


class F4_reference_heating_annual_energy_use(Variable):
    value_type = float
    entity = Building
    definition_period = ETERNITY
    label = 'What is the reference heating annual energy use for the AC, as' \
            ' defined in Table F4.4?'

    def formula(buildings, period, parameters):
        heating_capacity = buildings('heating_capacity', period)
        weather_zone = buildings('weather_zone', period)
        heating_hours = parameters(period).HEAB.F4.cooling_and_heating_hours.heating_hours[weather_zone]
        product_class = buildings('F4_product_class', period)
        baseline_heating_ACOP = parameters(period).HEAB.F4.baseline_AEER_and_ACOP.ACOP[product_class]
        return heating_capacity * heating_hours / baseline_heating_ACOP


class heating_capacity(Variable):
    value_type = float
    entity = Building
    definition_period = ETERNITY
    label = 'What is the heating capacity for Activity Definition F4?'


class F4_cooling_annual_energy_use(Variable):
    value_type = float
    entity = Building
    definition_period = ETERNITY
    label = 'What is the cooling annual energy use for the AC, as defined in' \
            ' Table F4.4?'

    def formula(buildings, period, parameters):
        cooling_power_input = buildings('cooling_power_input', period)
        weather_zone = buildings('weather_zone', period)
        cooling_hours = parameters(period).HEAB.F4.cooling_and_heating_hours.cooling_hours[weather_zone]
        cooling_annual_energy_use = cooling_power_input * cooling_hours
        return cooling_annual_energy_use


class cooling_power_input(Variable):
    value_type = float
    entity = Building
    definition_period = ETERNITY
    label = 'What is the cooling power input for Activity Definition F4?'


class F4_heating_annual_energy_use(Variable):
    value_type = float
    entity = Building
    definition_period = ETERNITY
    label = 'What is the heating annual energy use for the AC, as defined in' \
            ' Table F4.4?'

    def formula(buildings, period, parameters):
        heating_power_input = buildings('heating_power_input', period)
        weather_zone = buildings('weather_zone', period)
        heating_hours = parameters(period).HEAB.F4.cooling_and_heating_hours.heating_hours[weather_zone]
        heating_annual_energy_use = heating_power_input * heating_hours
        return heating_annual_energy_use


class heating_power_input(Variable):
    value_type = float
    entity = Building
    definition_period = ETERNITY
    label = 'What is the heating power input for Activity Definition F4?'


class WeatherZone(Enum):
    hot_zone = 'AC is installed in a hot zone.'
    average_zone = 'AC is installed in a average zone.'
    cold_zone = 'AC is installed in a cold zone.'


class weather_zone(Variable):
    value_type = Enum
    possible_values = WeatherZone
    default_value = WeatherZone.hot_zone
    entity = Building
    definition_period = ETERNITY
    label = 'What is the weather zone in which the AC for activity definition '\
            ' F4 is installed?'
