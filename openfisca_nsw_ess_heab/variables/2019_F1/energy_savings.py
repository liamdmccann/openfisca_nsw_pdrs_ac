# Import from openfisca-core the common Python objects used to code the legislation in OpenFisca
from openfisca_core.model_api import *
# Import the Entities specifically defined for this tax and benefit system
from openfisca_nsw_base.entities import *
import numpy as np


class F1_2019_deemed_equipment_electricity_savings(Variable):
    value_type = float
    entity = Building
    definition_period = ETERNITY
    label = 'What is the deemed equipment electricity savings for the' \
            ' installed product, as defined in Activity Definition F1?'

    def formula(buildings, period, parameters):
        baseline_efficiency = buildings('baseline_efficiency', period)
        total_electricity_consumption = buildings('total_energy_consumption', period)
        total_display_area = buildings('total_display_area', period)
        lifetime = buildings('lifetime', period)
        days_in_year = parameters(period).ESS_general.days_in_year
        kWh_to_MWh_conversion = parameters(period).unit_conversion_factors['kWh_to_MWh']
        electricity_savings = ((baseline_efficiency * total_display_area - total_electricity_consumption)
        * days_in_year * lifetime / kWh_to_MWh_conversion)
        return electricity_savings


class F1_2019_ESCs(Variable):
    value_type = float
    entity = Building
    definition_period = ETERNITY
    label = 'What is the deemed equipment electricity savings for the' \
            ' installed product, as defined in Activity Definition F1?'

    def formula(buildings, period, parameters):
        electricity_savings = buildings('F1_2019_deemed_equipment_electricity_savings', period)
        number_of_ESCs = electricity_savings * 1.06
        return np.floor(number_of_ESCs)
