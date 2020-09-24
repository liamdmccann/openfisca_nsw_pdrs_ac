# Import from openfisca-core the common Python objects used to code the legislation in OpenFisca
from openfisca_core.model_api import *
# Import the Entities specifically defined for this tax and benefit system
from openfisca_nsw_base.entities import *


class F6_motor_is_part_of_ducted_fan(Variable):
    value_type = bool
    entity = Building
    definition_period = ETERNITY
    label = 'Is the motor part of a ducted fan?'


class F6_motor_is_part_of_partition_fan(Variable):
    value_type = bool
    entity = Building
    definition_period = ETERNITY
    label = 'Is the motor part of a partition fan?'


class F6_fan_is_part_of_air_handling_system(Variable):
    value_type = bool
    entity = Building
    definition_period = ETERNITY
    label = 'Is the fan that the motor is being installed in part of an air' \
            ' handling system?'


class F6_ducted_or_partition_fan_part_of_air_handling_system(Variable):
    value_type = bool
    entity = Building
    definition_period = ETERNITY
    label = 'Is the motor part of a ducted fan or partition fan, in an air' \
            ' handling system?'

    def formula(buildings, period, parameters):
        part_of_ducted_fan = buildings('F6_motor_is_part_of_ducted_fan', period)
        part_of_partition_fan = buildings('F6_motor_is_part_of_partition_fan', period)
        part_of_air_handling_system = buildings('F6_fan_is_part_of_air_handling_system', period)
        return ((part_of_ducted_fan + part_of_partition_fan) * part_of_air_handling_system)


class F6_unit_replaces_equivalent_shaded_pole_motor_unit(Variable):
    value_type = bool
    entity = Building
    definition_period = ETERNITY
    label = 'Does the new End User Equipment replace an equivalent shaded pole' \
            ' motor unit?'


class F6_unit_replaces_permanent_split_capacitor_motor(Variable):
    value_type = bool
    entity = Building
    definition_period = ETERNITY
    label = 'Does the new End User Equipment replace a permanent split' \
            ' capacitor motor?'


class F6_replaces_equivalent_shaded_or_permanent_split_unit(Variable):
    value_type = bool
    entity = Building
    definition_period = ETERNITY
    label = 'Does the new End User Equipment replace an equivalent shaded pole' \
            ' or a permanent split capacitor motor?'

    def formula(buildings, period, parameters):
        replaces_shaded_pole_motor_unit = buildings('F6_unit_replaces_equivalent_shaded_pole_motor_unit', period)
        replaces_permanent_split_capacitor_motor = buildings('F6_unit_replaces_permanent_split_capacitor_motor', period)
        return (replaces_shaded_pole_motor_unit + replaces_permanent_split_capacitor_motor)


class F6_unit_installed_to_manufacturer_guidelines(Variable):
    value_type = bool
    entity = Building
    definition_period = ETERNITY
    label = 'Has the unit been installed according to manufacturer guidelines?'


class F6_unit_installed_to_administrator_requirements(Variable):
    value_type = bool
    entity = Building
    definition_period = ETERNITY
    label = 'Has the unit been installed according to any additional' \
            ' requirements set out by the Scheme Administrator?'


class F6_meets_installation_requirements(Variable):
    value_type = bool
    entity = Building
    definition_period = ETERNITY
    label = 'Does the installation meet the installation guidelines defined in' \
            ' Activity Definition F5?'

    def formula(buildings, period, parameters):
        is_part_of_air_handling_system = buildings('F6_ducted_or_partition_fan_part_of_air_handling_system', period)
        replaces_shaded_or_split_unit = buildings('F6_replaces_equivalent_shaded_or_permanent_split_unit', period)
        installed_according_to_manufacturer_guidelines = buildings('F6_unit_installed_to_administrator_requirements', period)
        installed_according_to_administrator_requirements = buildings('F6_unit_installed_to_administrator_requirements', period)
        return (installed_in_RC_freezer_or_cold_room * replaces_shaded_or_split_unit
        * installed_according_to_manufacturer_guidelines * installed_according_to_administrator_requirements)
