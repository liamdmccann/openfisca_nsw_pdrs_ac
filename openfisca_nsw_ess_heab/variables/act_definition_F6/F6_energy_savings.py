# Import from openfisca-core the common Python objects used to code the legislation in OpenFisca
from openfisca_core.model_api import *
# Import the Entities specifically defined for this tax and benefit system
from openfisca_nsw_base.entities import *


class F6_electricity_savings(Variable):
    value_type = float
    entity = Building
    definition_period = ETERNITY
    label = 'What is the electricity savings for the activity conducted within' \
            ' Activity Definition F6?'

    def formula(buildings, period, parameters):
        input_power = buildings('F6_input_power', period)
        nominal_input_power = select([input_power <= 34.00,
                                    input_power > 34.00],
                                    ["less_than_or_equal_to_34_kW",
                                    "more_than_34_kW"])
        coefficient_a = parameters(period).HEAB.F6.nominal_input_power.coefficient_a[nominal_input_power]
        coefficient_b = parameters(period).HEAB.F6.nominal_input_power.coefficient_b[nominal_input_power]
        control_system = buildings('F6_control_system', period)
        average_power = parameters(period).HEAB.F6.average_power[control_system]
        building_class = buildings('BCA_building_class')
        business_classification = buildings('business_classification')
        hours = parameters(period).HEAB.F6.hours[building_class][business_classification]
        lifetime = parameters(period).HEAB.F6.lifetime
        MWh_conversion = parameters(period).general_ESS.MWh_conversion
        electricity_savings = ((input_power * (coefficient_a - average_power) + coefficient_b)
                              * (1 + (1 / coefficient_of_performance))
                              * hours * lifetime / MWh_conversion)
        return electricity_savings


class F6ControlSystem(Enum):
    no_control_system = 'The motor has no control system in place.'
    temperature_dependent_speed_control = 'The motor has a temperature dependent' \
                                          ' speed control in place.'
    pressure_dependent_speed_control = 'The motor has a pressure dependent' \
                                       ' speed control in place.'
    timer_speed_control = 'The control system has a timer speed control, which' \
                          ' is set on the low speed setting for at least 8 hours' \
                          ' per day.'
    # note we need to determine what happens in the case where the timer is not \
    # set to a minimum of 8 hours on low speed per day.


class F6_control_system(Variable):
    value_type = Enum
    entity = Building
    possible_values = F6ControlSystem
    default_value = F6ControlSystem.no_control_system
    definition_period = ETERNITY
    label = 'What is the control system for the new end user equipment to be' \
            ' installed within Activity Definition F6?'


class F6RefrigeratorSystemType(Enum):
    refrigerated_cabinet = 'Motor is installed in a refrigerated cabinet.'
    reach_in_freezer = 'Motor is installed in a reach in freezer.'
    cool_room = 'Motor is installed in a cool room.'


class F6_refrigerator_type(Variable):
    value_type = Enum
    entity = Building
    possible_values = F6RefrigeratorSystemType
    default_value = F6RefrigeratorSystemType.refrigerated_cabinet
    definition_period = ETERNITY
    label = 'What is the refrigerator type that the new End User Equipment is' \
            ' being installed in, in Activity Definition F5?'


class F6_input_power(Variable):
    value_type = float
    entity = Building
    definition_period = ETERNITY
    label = 'What is the nominal input power of new End User Equipment at full' \
            ' throttle, with the impeller fitted?'
