# Import from openfisca-core the common Python objects used to code the legislation in OpenFisca
from openfisca_core.model_api import *
# Import the Entities specifically defined for this tax and benefit system
from openfisca_nsw_base.entities import *
import time
import numpy as np
import datetime

# note because this activity definition requires calculation based off years, \
# you need to import the above libraries to make it work

epoch = time.gmtime(0).tm_year
today_date_and_time = np.datetime64(datetime.datetime.now())
today = today_date_and_time.astype('datetime64[D]')


class F8_existing_end_user_equipment_is_single_gas_fired_steam_boiler(Variable):
    value_type = bool
    entity = Building
    definition_period = ETERNITY
    label = 'Is the existing end user equipment a single gas fired steam boiler?'


class F8_existing_end_user_equipment_is_multiple_gas_fired_steam_boilers(Variable):
    value_type = bool
    entity = Building
    definition_period = ETERNITY
    label = 'Is the existing end user equipment multiple gas fired steam boilers?'


class F8_is_not_residential_building(Variable):
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


class F8_existing_equipment_more_than_10_years_old(Variable):
    value_type = bool
    entity = Building
    definition_period = ETERNITY
    label = 'Is the existing end use equipment more than 10 years old?'

    def formula(buildings, period, parameters):
        existing_equipment_installation_date = buildings('F8_existing_equipment_installation_date', period)
        existing_equipment_age_in_days = ((today.astype('datetime64[D]') - existing_equipment_installation_date.astype('datetime64[D]')).astype('datetime64[D]'))
        existing_equipment_age = existing_equipment_age_in_days.astype('datetime64[Y]')
        return (existing_equipment_age.astype('int') > 10)
        # note that astype('int') converts the datetime64 object (YYYY-MM-DD) to a number \
        # for comparison against the minimum age of 10 years


class F8_existing_equipment_in_working_order(Variable):
    value_type = bool
    entity = Building
    definition_period = ETERNITY
    label = 'Is the existing end use equipment in working order?'


class F8_meets_eligibility_requirements(Variable):
    value_type = bool
    entity = Building
    definition_period = ETERNITY
    label = 'Does the equipment meet the Equipment Requirements of Activity' \
            ' Definition F7?'

    def formula(buildings, period, parameters):
        is_single_or_multiple_gas_fired_steam_boilers = (buildings('F8_existing_end_user_equipment_is_single_gas_fired_steam_boiler', period)
        + buildings('F8_existing_end_user_equipment_is_multiple_gas_fired_steam_boilers', period))
        not_in_residential_building = buildings('F8_is_not_residential_building', period)
        more_than_10_years_old = buildings('F8_existing_equipment_more_than_10_years_old', period)
        in_working_order = buildings('F8_existing_equipment_in_working_order', period)
        return (is_single_or_multiple_gas_fired_steam_boilers * not_in_residential_building
                * more_than_10_years_old * in_working_order)
