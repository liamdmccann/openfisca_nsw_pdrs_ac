# Import from openfisca-core the common Python objects used to code the legislation in OpenFisca
from openfisca_core.model_api import *
# Import the Entities specifically defined for this tax and benefit system
from openfisca_nsw_base.entities import *


class F4_deemed_equipment_electricity_savings(Variable):
    value_type = float
    entity = Building
    definition_period = ETERNITY
    label = 'Returns the equipment savings for installing a new AC through' \
            ' summing the cooling and heating capacity, in MWh.'

    def formula(buildings, period, parameters):
        cooling_energy_savings = buildings('cooling_energy_savings', period)
        heating_energy_savings = buildings('heating_energy_savings', period)
        return cooling_energy_savings + heating_energy_savings


class cooling_energy_savings(Variable):
    value_type = float
    entity = Building
    definition_period = ETERNITY
    label = 'Returns the cooling electricity savings associated with' \
            ' installing a High Efficiency Air Conditioner, as defined' \
            ' in Equation F4.2. Returns savings in MWh.'

    def formula(buildings, period, parameters):
        cooling_capacity = buildings('cooling_capacity', period)
        product_class = buildings('product_class', period)
        baseline_cooling_AEER = parameters(period).F4.MEPS_values[product_class]
        AEER = buildings('AEER', period)
        cooling_hours = parameters(period).F4.cooling_hours
        lifetime = parameters(period).F4.lifetime
        return (cooling_capacity / baseline_cooling_AEER
                - cooling_capacity / AEER) + cooling_hours * lifetime / 1000


class heating_energy_savings(Variable):
    value_type = float
    entity = Building
    definition_period = ETERNITY
    label = 'Returns the heating electricity savings associated with' \
            ' installing a High Efficiency Air Conditioner, as defined' \
            ' in Equation F4.2. Returns savings in MWh.'

    def formula(buildings, period, parameters):
        heating_capacity = buildings('heating_capacity', period)
        product_class = buildings('product_class', period)
        baseline_heating_ACOP = parameters(period).F4.MEPS_values[product_class]
        ACOP = buildings('ACOP', period)
        heating_hours = parameters(period).F4.heating_hours
        lifetime = parameters(period).F4.lifetime
        return (heating_capacity / baseline_heating_ACOP
                - heating_capacity / ACOP) + heating_hours * lifetime / 1000
