

#include <Adafruit_GFX.h>
#include <Adafruit_SSD1306.h>
#include "common.h"
static const unsigned char PROGMEM tool_icon16x16[] = {
    0b00000000, 0b00000000, //
    0b00000000, 0b01100000, //          ##
    0b00000000, 0b11100000, //         ###
    0b00000001, 0b11000000, //        ###
    0b00000001, 0b11000000, //        ###
    0b00000001, 0b11100110, //        ####  ##
    0b00000011, 0b11111110, //       #########
    0b00000111, 0b11111100, //      #########
    0b00001111, 0b11111000, //     #########
    0b00011111, 0b11000000, //    #######
    0b00111111, 0b10000000, //   #######
    0b01111111, 0b00000000, //  #######
    0b11111110, 0b00000000, // #######
    0b11111100, 0b00000000, // ######
    0b11111000, 0b00000000, // #####
    0b01110000, 0b00000000, //  ###
};

static const unsigned char PROGMEM icon_clear[] = {
    0b00000000, 0b00000000, //
    0b00000000, 0b00000000, //
    0b00000000, 0b00000000, //
    0b00000001, 0b00000000, //
    0b00000001, 0b00000000, //
    0b00000001, 0b00000000, //
    0b00000000, 0b00000000, //
    0b00000000, 0b00000000, //
    0b00000000, 0b00000000, //
    0b00000000, 0b00000000, //
    0b00000000, 0b00000000, //
    0b00000000, 0b00000000, //
    0b00000000, 0b00000000, //
    0b00000000, 0b00000000, //
    0b00000000, 0b00000000, //
    0b00000000, 0b00000000, //
};

unsigned char humidity2_icon16x16[] = {
    0b00000000, 0b00000000, //
    0b00000001, 0b10000000, //        ##
    0b00000011, 0b11000000, //       ####
    0b00000111, 0b11100000, //      ######
    0b00001111, 0b11110000, //     ########
    0b00001111, 0b11110000, //     ########
    0b00011111, 0b11111000, //    ##########
    0b00011111, 0b11011000, //    ####### ##
    0b00111111, 0b10011100, //   #######  ###
    0b00111111, 0b10011100, //   #######  ###
    0b00111111, 0b00011100, //   ######   ###
    0b00011110, 0b00111000, //    ####   ###
    0b00011111, 0b11111000, //    ##########
    0b00001111, 0b11110000, //     ########
    0b00000011, 0b11000000, //       ####
    0b00000000, 0b00000000, //
};

unsigned char humidity_icon16x16[] = {
    0b00000000, 0b00000000, //
    0b00000001, 0b10000000, //        ##
    0b00000011, 0b11000000, //       ####
    0b00000111, 0b11100000, //      ######
    0b00001110, 0b01110000, //     ###  ###
    0b00001100, 0b00110000, //     ##    ##
    0b00011100, 0b00111000, //    ###    ###
    0b00011000, 0b00011000, //    ##      ##
    0b00111000, 0b00011100, //   ###      ###
    0b00111000, 0b00011100, //   ###      ###
    0b00111000, 0b00011100, //   ###      ###
    0b00011100, 0b00111000, //    ###    ###
    0b00011111, 0b11111000, //    ##########
    0b00001111, 0b11110000, //     ########
    0b00000011, 0b11000000, //       ####
    0b00000000, 0b00000000, //
};

unsigned char temperature_icon16x16[] = {
    0b00000001, 0b11000000, //        ###
    0b00000011, 0b11100000, //       #####
    0b00000111, 0b00100000, //      ###  #
    0b00000111, 0b11100000, //      ######
    0b00000111, 0b00100000, //      ###  #
    0b00000111, 0b11100000, //      ######
    0b00000111, 0b00100000, //      ###  #
    0b00000111, 0b11100000, //      ######
    0b00000111, 0b00100000, //      ###  #
    0b00001111, 0b11110000, //     ########
    0b00011111, 0b11111000, //    ##########
    0b00011111, 0b11111000, //    ##########
    0b00011111, 0b11111000, //    ##########
    0b00011111, 0b11111000, //    ##########
    0b00001111, 0b11110000, //     ########
    0b00000111, 0b11100000, //      ######
};
unsigned char home_icon16x16[] =
    {
        0b00000111, 0b11100000, //      ######
        0b00001111, 0b11110000, //     ########
        0b00011111, 0b11111000, //    ##########
        0b00111111, 0b11111100, //   ############
        0b01111111, 0b11111110, //  ##############
        0b11111111, 0b11111111, // ################
        0b11000000, 0b00000011, // ##            ##
        0b11000000, 0b00000011, // ##            ##
        0b11000000, 0b00000011, // ##            ##
        0b11001111, 0b11110011, // ##  ########  ##
        0b11001111, 0b11110011, // ##  ########  ##
        0b11001100, 0b00110011, // ##  ##    ##  ##
        0b11001100, 0b00110011, // ##  ##    ##  ##
        0b11001100, 0b00110011, // ##  ##    ##  ##
        0b11111100, 0b00111111, // ######    ######
        0b11111100, 0b00111111, // ######    ######
};

unsigned char wifi2_icon16x16[] = {
    0b00000000, 0b00000000, //
    0b00000111, 0b11100000, //      ######
    0b00011111, 0b11111000, //    ##########
    0b00111111, 0b11111100, //   ############
    0b01110000, 0b00001110, //  ###        ###
    0b01100111, 0b11100110, //  ##  ######  ##
    0b00001111, 0b11110000, //     ########
    0b00011000, 0b00011000, //    ##      ##
    0b00000011, 0b11000000, //       ####
    0b00000111, 0b11100000, //      ######
    0b00000100, 0b00100000, //      #    #
    0b00000001, 0b10000000, //        ##
    0b00000001, 0b10000000, //        ##
    0b00000000, 0b00000000, //
    0b00000000, 0b00000000, //
    0b00000000, 0b00000000, //
};

extern Adafruit_SSD1306 display;
void main_page(void)
{
    display.clearDisplay();
    display.drawBitmap(0, 0, tool_icon16x16, 16, 16, SSD1306_WHITE);
    display.drawBitmap(128 - 16, 0, wifi2_icon16x16, 16, 16, SSD1306_WHITE);
    display.setTextSize(1);
    display.setTextColor(INVERSE);
    display.setCursor((SCREEN_WIDTH - 6 * 9) / 2, 0);
    display.println("Main page");
    display.drawLine(0, 16, 128, 16, SSD1306_WHITE);
    display.setCursor(kX_ELEMENTS_START, kY_ELEMENTS_START);
    // display.setFont(&FreeMono9pt7b);
    display.setTextSize(0);
    display.println("Temp:");
    display.setCursor(kX_ELEMENTS_START, kY_ELEMENTS_START + kY_STEP);
    display.println("Humi:");
    // display.setFont(NULL);
    display.setCursor(kX_ELEMENTS_START, kY_ELEMENTS_START + kY_STEP * 2);
    display.println("Pres:");
    // icon display
    display.drawBitmap(kX_ELEMENTS_START + kX_STEP * 2, kY_ELEMENTS_START, temperature_icon16x16, 16, 16, SSD1306_WHITE);
    display.drawBitmap(kX_ELEMENTS_START + kX_STEP * 2, kY_ELEMENTS_START + kY_STEP, humidity2_icon16x16, 16, 16, SSD1306_WHITE);

    display.display();
    // // Invert and restore display, pausing in-between
    // display.invertDisplay(true);
    // delay(1000);
    // display.invertDisplay(false);
    // delay(1000);
    main_page_display_process(85, 50, 1000);
    delay(2000);
}

void main_page_display_process(uint16_t temp, uint16_t humi, uint16_t pres)
{
    char buffer[20];
    memset(buffer, 0x00, sizeof(buffer));
    display.setCursor(50, kY_ELEMENTS_START + 4);
    display.setFont(&FreeMono9pt7b);
    sprintf(buffer, "%d*F", temp);
    display.print(buffer);
    memset(buffer, 0x00, sizeof(buffer));

    display.setCursor(50, kY_ELEMENTS_START * 2 + 8);
    display.setFont(&FreeMono9pt7b);
    sprintf(buffer, "%d%s", humi, "%");
    display.print(buffer);
    memset(buffer, 0x00, sizeof(buffer));

    display.setCursor(50, kY_ELEMENTS_START * 3 + 2);
    display.setFont(NULL);
    sprintf(buffer, "%d hPa", pres);
    display.print(buffer);
    display.display();
}