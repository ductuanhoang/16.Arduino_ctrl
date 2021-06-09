/*
 * Common.h
 *
 *  Created on: Apr 24, 2021
 *      Author: ductu
 */

#ifndef MAIN_COMMON_H_
#define MAIN_COMMON_H_

/****************************************************************************/
/***        Include files                                                 ***/
/****************************************************************************/

/****************************************************************************/
/***        Macro Definitions                                             ***/
/****************************************************************************/

/****************************************************************************/
/***        Type Definitions                                              ***/
/****************************************************************************/

/****************************************************************************/
/***         Exported global functions                                     ***/
/****************************************************************************/

#include <string.h>
#include <stdio.h>
#include <stdlib.h>
#include <stdint.h>
#include <stddef.h>
#include <stdbool.h>

typedef enum e_setting_page
{
    E_SETTING_TEMP,
    E_SETTING_FOG,
    E_SETTING_CO2,
};

typedef struct
{
    /* data */
    uint16_t setup;
    uint16_t high_alram;
    uint16_t low_alram;
    uint16_t up_lag;
    uint16_t down_lag;
} setting_t;

typedef struct
{
    /* data */
    setting_t temerature;
    setting_t humidity;
    setting_t Co2;
    setting_t Fog;
} setting_param_t;

typedef struct
{
    float temperature;
    float humidity;
    float Co2;
} sensor_value_t;

typedef enum
{
    E_BUTTON_NONE = 0,
    E_BUTTON_UP = 1,
    E_BUTTON_DOWN,
    E_BUTTON_RIGHT,
    E_BUTTON_LEFT,
    E_BUTTON_SELECT,
}e_buttons_name;

extern setting_param_t setting_param;
extern sensor_value_t sensor_value;
#endif /* MAIN_COMMON_H_ */
