#ifndef _COMMON_H_
#define _COMMON_H_
#include <stdint.h>

#define kX_ELEMENTS_START 0
#define kY_ELEMENTS_START 20
#define kY_STEP 18
#define kX_STEP 15

#define kICon_START 21

#define LOGO_HEIGHT 16
#define LOGO_WIDTH 16
#define SCREEN_WIDTH 128 // OLED display width, in pixels
#define SCREEN_HEIGHT 64 // OLED display height, in pixels

typedef struct
{
    /* data */
    uint16_t setup;
    uint16_t high_alram;
    uint16_t low_alram;
} setting_t;

typedef struct
{
    /* data */
    setting_t temerature;
    setting_t humidity;
    setting_t Co2;
} setting_param_t;
setting_param_t setting_param;
#endif