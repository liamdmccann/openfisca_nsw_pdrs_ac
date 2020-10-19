# Import from openfisca-core the common Python objects used to code the legislation in OpenFisca
from openfisca_core.model_api import *
# Import the Entities specifically defined for this tax and benefit system
from openfisca_nsw_base.entities import *


class F10_existing_end_user_equipment_is_gas_fired_steam_boiler(Variable):
    value_type = bool
    entity = Building
    definition_period = ETERNITY
    label = 'Is the existing end user equipment a gas fired steam boiler?'


class F10_existing_end_user_equipment_is_hot_water_boiler(Variable):
    value_type = bool
    entity = Building
    definition_period = ETERNITY
    label = 'Is the existing end user equipment a fired hot water boiler?'


class F10_existing_end_user_equipment_is_water_heater(Variable):
    value_type = bool
    entity = Building
    definition_period = ETERNITY
    label = 'Is the existing end user equipment a fired water heater?'


class F10_is_not_residential_building(Variable):
    value_type = bool
    entity = Building
    definition_period = ETERNITY
    label = 'Is the existing end user equipment installed at a BCA Class 2, 3,' \
            ' 5, 6, 7, 8, 9 or 10 building - i.e, not a residential building?'

    def formula(buildings, period, parameters):
        BCA_building_class = buildings('BCA_building_class', period)
        BCABuildingClass = BCA_building_class.possible_values
        in_BCA_Class_2 = (BCA_building_class == BCABuildingClass.BCA_Class_2)
        in_BCA_Class_3 = (BCA_building_class == BCABuildingClass.BCA_Class_3)
        in_BCA_Class_5 = (BCA_building_class == BCABuildingClass.BCA_Class_5)
        in_BCA_Class_6_shop = (BCA_building_class == BCABuildingClass.BCA_Class_6_shop)
        in_BCA_Class_6_cafe_or_rest = (BCA_building_class == BCABuildingClass.BCA_Class_6_cafe_or_rest)
        in_BCA_Class_7a = (BCA_building_class == BCABuildingClass.BCA_Class_7a)
        in_BCA_Class_7b = (BCA_building_class == BCABuildingClass.BCA_Class_7b)
        in_BCA_Class_8 = (BCA_building_class == BCABuildingClass.BCA_Class_8)
        in_BCA_Class_9a_clinic = (BCA_building_class == BCABuildingClass.BCA_Class_9a_clinic)
        in_BCA_Class_9a_hospital = (BCA_building_class == BCABuildingClass.BCA_Class_9a_hospital)
        in_BCA_Class_9b_schools = (BCA_building_class == BCABuildingClass.BCA_Class_9b_schools)
        in_BCA_Class_9b_theatres = (BCA_building_class == BCABuildingClass.BCA_Class_9b_theatres)
        in_BCA_Class_10a = (BCA_building_class == BCABuildingClass.BCA_Class_10a)
        in_BCA_Class_10b = (BCA_building_class == BCABuildingClass.BCA_Class_10b)
        in_BCA_Class_10c = (BCA_building_class == BCABuildingClass.BCA_Class_10c)
        return (in_BCA_Class_2 + in_BCA_Class_3 + in_BCA_Class_5 + in_BCA_Class_6_shop
                + in_BCA_Class_6_cafe_or_rest + in_BCA_Class_7a + in_BCA_Class_7b
                + in_BCA_Class_8 + in_BCA_Class_9a_clinic + in_BCA_Class_9a_hospital
                + in_BCA_Class_9b_schools + in_BCA_Class_9b_theatres + in_BCA_Class_10a
                + in_BCA_Class_10b + in_BCA_Class_10c)
        # in retrospect, probably cleaner to just code in the residential enum responses \
        # and then use a not variable?


class F10_replaces_existing_end_user_equipment(Variable):
    value_type = bool
    entity = Building
    definition_period = ETERNITY
    label = 'Does the equipment replace existing End User Equipment?'


class F10_has_digital_burner_control_system(Variable):
    value_type = bool
    entity = Building
    definition_period = ETERNITY
    label = 'Does the equipment have a digital burner control system installed?'


class F10_digital_burner_control_system_will_be_installed(Variable):
    value_type = bool
    entity = Building
    definition_period = ETERNITY
    label = 'Will a digital burner control system be installed?'


class F10_meets_eligibility_requirements(Variable):
    value_type = bool
    entity = Building
    definition_period = ETERNITY
    label = 'Does the equipment meet the Equipment Requirements of Activity' \
            ' Definition F7?'

    def formula(buildings, period, parameters):
        is_gas_fired_steam_boiler = buildings('F10_existing_end_user_equipment_is_gas_fired_steam_boiler', period)
        is_hot_water_boiler = buildings('F10_existing_end_user_equipment_is_hot_water_boiler', period)
        is_water_heater = buildings('F10_existing_end_user_equipment_is_water_heater', period)
        is_not_residential = buildings('F10_is_not_residential_building', period)
        replaces_existing_end_user_equipment = buildings('F10_replaces_existing_end_user_equipment', period)
        has_digital_burner_control_system = buildings('F10_has_digital_burner_control_system', period)
        digital_burner_control_system_will_be_installed = buildings('F10_digital_burner_control_system_will_be_installed', period)
        return ((is_gas_fired_steam_boiler + is_hot_water_boiler + is_water_heater) * is_not_residential
                * (not(replaces_existing_end_user_equipment))
                * (has_digital_burner_control_system + digital_burner_control_system_will_be_installed))
