
#include "Common.h"

#define ON 1
#define OFF 0

bool heater_status = OFF;
bool fog_status = OFF;
bool fan_status = OFF;
static void heater_control(bool status)
{
    if (status == ON)
    {
    }
    else if (status == OFF)
    {
    }
    heater_status = status;
}
static void fog_control(bool status)
{
    if (status == ON)
    {
    }
    else if (status == OFF)
    {
    }
    fog_status = status;
}

static void fan_control(bool status)
{
    if (status == ON)
    {
    }
    else if (status == OFF)
    {
    }
}
// call in loop
void action_heat(void)
{
    if (sensor_value.temperature <= (setting_param.temerature.setup - setting_param.temerature.down_lag))
    {
        heater_control(ON);
    }
    else if (sensor_value.temperature >= setting_param.temerature.setup)
    {
        heater_control(OFF);
    }
}
// call in loop
void action_fog(void)
{
    if (sensor_value.humidity <= (setting_param.humidity.setup - setting_param.humidity.down_lag))
    {
        fog_control(ON);
    }
    else if (sensor_value.humidity >= setting_param.humidity.setup)
    {
        fog_control(OFF);
    }
}
// call in loop
void action_fan(void)
{
    if (heater_status == ON)
    {
        fan_status = ON;
    }
    else if (fog_status == ON)
    {
        fan_status = ON;
    }
    else if (sensor_value.temperature >= (setting_param.temerature.setup + setting_param.temerature.up_lag))
    {
        fan_status = ON;
    }
    else if (sensor_value.humidity >= (setting_param.Fog.setup + setting_param.Fog.up_lag))
    {
        fan_status = ON;
    }
    else if (sensor_value.Co2 >= (setting_param.Co2.setup + setting_param.Co2.up_lag))
    {
        fan_status = ON;
    }
    else if (sensor_value.temperature <= setting_param.temerature.setup)
    {
        fan_status = OFF;
    }
    else if (sensor_value.humidity <= setting_param.Fog.setup)
    {
        fan_status = OFF;
    }
    else if (sensor_value.Co2 <= setting_param.Co2.setup)
    {
        fan_status = OFF;
    }

    fan_control(fan_status);
}

void action_process(void)
{
    action_fan();
    action_fog();
    action_heat();
}