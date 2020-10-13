# Import from openfisca-core the common Python objects used to code the legislation in OpenFisca
from openfisca_core.model_api import *
# Import the Entities specifically defined for this tax and benefit system
from openfisca_nsw_base.entities import *


class F1_5_electricity_savings(Variable):
    value_type = float
    entity = Building
    definition_period = ETERNITY
    label = 'What is the electricity savings for the activity conducted within' \
            ' Activity Definition F1.1?'

    def formula(buildings, period, parameters):
        total_electricity_consumption = buildings('F1_5_daily_total_electricity_consumption', period)
        net_volume = buildings('F1_5_net_volume', period)
        product_class = buildings('F1_product_class', period)
        is_chiller = buildings('is_chiller', period)
        is_freezer = buildings('is_freezer', period)
        duty_class = buildings('duty_class', period)
        is_chiller_or_freezer = select([(is_chiller),
                                        (is_freezer)],
                                       ['chiller',
                                        'freezer'])
        baseline_EEI = parameters(period).HEAB.F1.F1_5_baseline_EEIs.EEI[product_class][duty_class]
        m_coefficient = parameters(period).HEAB.F1.F1_5_coefficients.M[product_class]
        n_coefficient = parameters(period).HEAB.F1.F1_5_coefficients.N[product_class]
        adjustment_factor = parameters(period).HEAB.F1.F1_5_adjustment_factor[duty_class][is_chiller_or_freezer]
        days_in_year = parameters(period).general_ESS.days_in_year
        lifetime = parameters(period).HEAB.F1.F1_5_lifetime[product_class]
        MWh_conversion = parameters(period).general_ESS.unit_conversion_factors['kWh_to_MWh']
        return ((((baseline_EEI * ((m_coefficient * net_volume) + n_coefficient) / 100)
               - (total_electricity_consumption * adjustment_factor * days_in_year))
               * lifetime) / MWh_conversion)


class F1_5_daily_total_electricity_consumption(Variable):
    value_type = float
    entity = Building
    definition_period = ETERNITY
    label = 'What is the daily total energy consumption for the new RDC, as' \
            ' determined using GEMS 2019 s12 and recorded in the GEMS Registry?'


class F1_5_net_volume(Variable):
    value_type = float
    entity = Building
    definition_period = ETERNITY
    label = 'What is the net volume for the new RDC, as determined' \
            ' using GEMS 2019 s12 and recorded in the GEMS Registry?'
