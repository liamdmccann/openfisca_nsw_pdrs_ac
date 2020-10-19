# Import from openfisca-core the common Python objects used to code the legislation in OpenFisca
from openfisca_core.model_api import *
# Import the Entities specifically defined for this tax and benefit system
from openfisca_nsw_base.entities import *
import time
import numpy as np
import datetime
from datetime import datetime as py_datetime

# note because this activity definition requires calculation based off years, \
# you need to import the above libraries to make it work

epoch = time.gmtime(0).tm_year
today_date_and_time = np.datetime64(datetime.datetime.now())
today = today_date_and_time.astype('datetime64[D]')


class F15_is_installed_on_single_gas_fired_steam_boiler(Variable):
    value_type = bool
    entity = Building
    definition_period = ETERNITY
    label = 'Is the existing end user equipment installed on a single gas fired' \
            ' steam boiler?'


class F15_is_installed_on_multiple_gas_fired_steam_boilers(Variable):
    value_type = bool
    entity = Building
    definition_period = ETERNITY
    label = 'Is the existing end user equipment installed on multiple gas fired' \
            ' steam boilers?'


class F15_is_not_residential_building(Variable):
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


class F15_has_existing_sensor_based_blowdown_control(Variable):
    value_type = bool
    entity = Building
    definition_period = ETERNITY
    label = 'Does the equipment have an existing sensor based blowdown control?'


class F15_sensor_based_blowdown_control_installed_at_commissioning(Variable):
    value_type = bool
    entity = Building
    definition_period = ETERNITY
    label = 'Does the equipment have a sensor based blowdown control installed' \
            ' at the time of commissioning the End User Equipment?'


class F15_replaces_existing_end_user_equipment(Variable):
    value_type = bool
    entity = Building
    definition_period = ETERNITY
    label = 'Does the equipment replace existing End User Equipment?'


class F15_fluid_stream_below_40C_available_at_all_times(Variable):
    value_type = bool
    entity = Building
    definition_period = ETERNITY
    label = 'Is there a fluid stream, below 40C, available at all times to transfer heat from the boiler blowdown?'


class F15_meets_eligibility_requirements(Variable):
    value_type = bool
    entity = Building
    definition_period = ETERNITY
    label = 'Does the equipment meet the Equipment Requirements of Activity' \
            ' Definition F7?'

    def formula(buildings, period, parameters):
        installed_on_single_gas_fired_steam_boiler = buildings('F15_is_installed_on_single_gas_fired_steam_boiler', period)
        installed_on_multiple_gas_fired_steam_boilers = buildings('F15_is_installed_on_multiple_gas_fired_steam_boilers', period)
        is_not_residential = buildings('F15_is_not_residential_building', period)
        replaces_existing_equipment = buildings('F15_replaces_existing_end_user_equipment', period)
        has_existing_blowdown_control = buildings('F15_has_existing_sensor_based_blowdown_control', period)
        had_blowdown_at_commissioning = buildings('F15_sensor_based_blowdown_control_installed_at_commissioning', period)
        fluid_stream_available = buildings('F15_fluid_stream_below_40C_available_at_all_times', period)
        return ((installed_on_single_gas_fired_steam_boiler + installed_on_multiple_gas_fired_steam_boilers)
               * is_not_residential * (not(replaces_existing_equipment))
               * (has_existing_blowdown_control + had_blowdown_at_commissioning)
               * fluid_stream_available)
