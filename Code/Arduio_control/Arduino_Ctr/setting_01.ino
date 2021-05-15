#include <Adafruit_GFX.h>
#include <Adafruit_SSD1306.h>

extern Adafruit_SSD1306 display;
void setting_01_page(void)
{
    display.clearDisplay();
    display.drawBitmap(0, 0, tool_icon16x16, 16, 16, SSD1306_WHITE);
    display.drawBitmap(128 - 16, 0, wifi2_icon16x16, 16, 16, SSD1306_WHITE);
    display.setTextSize(1);
    display.setTextColor(INVERSE);
    display.setCursor((SCREEN_WIDTH - 10 * 9) / 2, 0);
    display.println("Setting page 01");
    display.drawLine(0, 16, 128, 16, SSD1306_WHITE);
    display.display();

    setting_display_process();
}

void setting_display_process(void)
{
    char buffer[20];
    display.setFont(NULL);
    memset(buffer, 0x00, sizeof(buffer));
    display.setCursor(20, 16 + 4);
    sprintf(buffer, "->Temp");
    display.print(buffer);
    memset(buffer, 0x00, sizeof(buffer));

    display.setCursor(20, 16 * 2 + 8);
    sprintf(buffer, "->Humi");
    display.print(buffer);
    memset(buffer, 0x00, sizeof(buffer));

    display.setCursor(20, 16 * 3 + 2);

    sprintf(buffer, "->C02");
    display.print(buffer);
    display.display();
}