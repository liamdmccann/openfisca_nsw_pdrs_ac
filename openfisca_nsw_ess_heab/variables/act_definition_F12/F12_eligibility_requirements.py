# Import from openfisca-core the common Python objects used to code the legislation in OpenFisca
from openfisca_core.model_api import *
# Import the Entities specifically defined for this tax and benefit system
from openfisca_nsw_base.entities import *


class F12_existing_end_user_equipment_installed_on_gas_fired_steam_boiler(Variable):
    value_type = bool
    entity = Building
    definition_period = ETERNITY
    label = 'Is the existing end user equipment installed on a gas fired' \
            ' steam boiler?'


class F12_existing_end_user_equipment_installed_on_hot_water_boiler(Variable):
    value_type = bool
    entity = Building
    definition_period = ETERNITY
    label = 'Is the existing end user equipment installed on a hot water boiler?'


class F12_existing_end_user_equipment_installed_on_water_heater(Variable):
    value_type = bool
    entity = Building
    definition_period = ETERNITY
    label = 'Is the existing end user equipment installed on a water heater?'


class F12_is_not_residential_building(Variable):
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


class F12_replaces_existing_end_user_equipment(Variable):
    value_type = bool
    entity = Building
    definition_period = ETERNITY
    label = 'Does the equipment replace existing End User Equipment?'


class F12_existing_steam_boiler_is_condensing_boiler(Variable):
    value_type = bool
    entity = Building
    definition_period = ETERNITY
    label = 'Is the existing steam boiler a condenser boiler?'


class F12_existing_hot_water_boiler_is_condensing_boiler(Variable):
    value_type = bool
    entity = Building
    definition_period = ETERNITY
    label = 'Is the existing hot water boiler a condenser boiler?'


class F12_existing_water_heater_is_condensing_heater(Variable):
    value_type = bool
    entity = Building
    definition_period = ETERNITY
    label = 'Is the existing water heater a condenser heater?'


class F12_is_heating_feedwater_stream(Variable):
    value_type = bool
    entity = Building
    definition_period = ETERNITY
    label = 'Is the End Use Equipment pre-heating a feedwater stream?'


class F12_has_heat_rejection_stream(Variable):
    value_type = bool
    entity = Building
    definition_period = ETERNITY
    label = 'Does the End User Equipment have a heat rejection stream, available' \
            ' for at least 80% of the operating time of the steam boiler,' \
            ' hot water boiler or water heater?'


class F12_meets_eligibility_requirements(Variable):
    value_type = bool
    entity = Building
    definition_period = ETERNITY
    label = 'Does the equipment meet the Equipment Requirements of Activity' \
            ' Definition F7?'

    def formula(buildings, period, parameters):
        installed_on_gas_fired_steam_boiler = buildings('F12_existing_end_user_equipment_installed_on_gas_fired_steam_boiler', period)
        installed_on_water_boiler = buildings('F12_existing_end_user_equipment_installed_on_hot_water_boiler', period)
        installed_on_water_heater = buildings('F12_existing_end_user_equipment_installed_on_water_heater', period)
        is_not_residential = buildings('F12_is_not_residential_building', period)
        replaces_existing_equipment = buildings('F12_replaces_existing_end_user_equipment', period)
        is_condensing_steam_boiler = buildings('F12_existing_steam_boiler_is_condensing_boiler', period)
        is_condensing_hot_water_boiler = buildings('F12_existing_hot_water_boiler_is_condensing_boiler', period)
        is_condensing_heater = buildings('F12_existing_water_heater_is_condensing_heater', period)
        has_heating_feedwater_stream = buildings('F12_is_heating_feedwater_stream', period)
        has_heat_rejection_stream = buildings('F12_has_heat_rejection_stream', period)
        return ((installed_on_gas_fired_steam_boiler + installed_on_water_boiler + installed_on_water_heater)
                * is_not_residential * (not(replaces_existing_equipment))
                * ((not(is_condensing_steam_boiler)) * (not(is_condensing_hot_water_boiler)) * (not(is_condensing_heater)))
                * (has_heating_feedwater_stream + ((not(has_heating_feedwater_stream)) * has_heat_rejection_stream)))
