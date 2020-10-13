# Import from openfisca-core the common Python objects used to code the legislation in OpenFisca
from openfisca_core.model_api import *
# Import the Entities specifically defined for this tax and benefit system
from openfisca_nsw_base.entities import *


class F8_existing_equipment_is_disconnected(Variable):
    value_type = bool
    entity = Building
    definition_period = ETERNITY
    label = 'Has the existing equipment been disconnected?'


class F8_existing_equipment_is_removed(Variable):
    value_type = bool
    entity = Building
    definition_period = ETERNITY
    label = 'Has the existing equipment been removed?'


class F8_disconnection_and_removal_performed_or_supervised_by_qualified_person(Variable):
    value_type = bool
    entity = Building
    definition_period = ETERNITY
    label = 'Are any disconnection and removal activities performed or supervised' \
            ' by a qualified person in accordance with relevant standards and legislation?'


class F8_meets_implementation_requirements(Variable):
    value_type = bool
    entity = Building
    definition_period = ETERNITY
    label = 'Does the equipment meet the Equipment Requirements of Activity' \
            ' Definition F7?'

    def formula(buildings, period, parameters):
        is_disconnected = buildings('F8_existing_equipment_is_disconnected', period)
        is_removed = buildings('F8_existing_equipment_is_removed', period)
        performed_or_supervised_by_qualified_person = buildings('F8_disconnection_and_removal_performed_or_supervised_by_qualified_person', period)
        return is_disconnected * is_removed * performed_or_supervised_by_qualified_person
