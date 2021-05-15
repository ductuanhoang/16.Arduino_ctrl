
#include "main_display.h"
#include "common.h"
#include <SPI.h>
#include <Wire.h>
#include <Adafruit_GFX.h>
#include <Adafruit_SSD1306.h>
#include <Fonts/FreeMono9pt7b.h>

#define OLED_MOSI 23
#define OLED_CLK 18
#define OLED_DC 22
#define OLED_CS 5
#define OLED_RESET 19

Adafruit_SSD1306 display(SCREEN_WIDTH, SCREEN_HEIGHT,
                         OLED_MOSI, OLED_CLK, OLED_DC, OLED_RESET, OLED_CS);

void setup()
{
    Serial.begin(115200);
    Serial.println(F("SSD1306 call"));

    // SSD1306_SWITCHCAPVCC = generate display voltage from 3.3V internally
    if (!display.begin(SSD1306_SWITCHCAPVCC))
    {
        Serial.println(F("SSD1306 allocation failed"));
        for (;;)
            ; // Don't proceed, loop forever
    }
    main_page();
    // setting_01_page();
}

void loop()
{
    // main_page_display_process(70, 40, 1000);
    delay(1000);
}

void setting_default_param(void)
{
    setting_param.temerature.setup = 80;
    setting_param.temerature.high_alram = 95;
    setting_param.temerature.low_alram = 65;

    setting_param.humidity.setup = 80;
    setting_param.humidity.high_alram = 110;
    setting_param.humidity.low_alram = 50;

    setting_param.Co2.setup = 500;
    setting_param.Co2.high_alram = 9000;
    setting_param.Co2.low_alram = 0; // un use
}

void setting_gpio(void)
{
}