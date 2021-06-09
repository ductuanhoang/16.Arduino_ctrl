#include "setting_icon.h"
#include <lvgl.h>
#include <TFT_eSPI.h>

#include "menu.h"
#include "menu_select.h"
#include "volume_mute.h"
#include "volume_run.h"
#include "humidity_icon.h"
#include "temperature_f.h"
#include "co2_icon.h"
#include "fan_icon_red.h"
#include "fan_icon_blue.h"
#include "heater_on.h"
#include "fog_on.h"
#include "Common.h"
#include "esp_system.h"
#include "esp_adc_cal.h"
#include "driver/adc.h"

TFT_eSPI tft = TFT_eSPI(); /* TFT instance */
static lv_disp_buf_t disp_buf;
static lv_color_t buf[LV_HOR_RES_MAX * 10];

#if USE_LV_LOG != 0
/* Serial debugging */
void my_print(lv_log_level_t level, const char *file, uint32_t line, const char *dsc)
{

    Serial.printf("%s@%d->%s\r\n", file, line, dsc);
    Serial.flush();
}
#endif

setting_param_t setting_param;
sensor_value_t sensor_value;

void setting_default_param(void)
{
    setting_param.temerature.setup = 80;
    setting_param.temerature.high_alram = 95;
    setting_param.temerature.low_alram = 65;
    setting_param.temerature.up_lag = 2;
    setting_param.temerature.down_lag = 2;

    setting_param.humidity.setup = 80;
    setting_param.humidity.high_alram = 110;
    setting_param.humidity.low_alram = 50;

    setting_param.Co2.setup = 500;
    setting_param.Co2.high_alram = 9000;
    setting_param.Co2.low_alram = 0; // un use
    setting_param.Co2.down_lag = 20;
    setting_param.Co2.up_lag = 20;

    setting_param.Fog.setup = 80;
    setting_param.Fog.up_lag = 3;
    setting_param.Fog.down_lag = 3;
    setting_param.Fog.high_alram = 95;
    setting_param.Fog.low_alram = 60;
}

/* Display flushing */
void my_disp_flush(lv_disp_drv_t *disp, const lv_area_t *area, lv_color_t *color_p)
{
    uint32_t w = (area->x2 - area->x1 + 1);
    uint32_t h = (area->y2 - area->y1 + 1);

    tft.startWrite();
    tft.setAddrWindow(area->x1, area->y1, w, h);
    tft.pushColors((uint16_t *)&color_p->full, w * h, true);
    tft.endWrite();

    lv_disp_flush_ready(disp);
}

/* Reading input device (simulated encoder here) */
bool read_encoder(lv_indev_drv_t *indev, lv_indev_data_t *data)
{
    static int32_t last_diff = 0;
    int32_t diff = 0;                   /* Dummy - no movement */
    int btn_state = LV_INDEV_STATE_REL; /* Dummy - no press */

    data->enc_diff = diff - last_diff;

    data->state = btn_state;

    last_diff = diff;

    return false;
}

lv_obj_t *imgbtn1;
lv_obj_t *label4;
lv_obj_t *label5;

void setup()
{
    Serial.begin(115200); /* prepare for possible serial debug */
    buttons_init();
    lv_init();

#if USE_LV_LOG != 0
    lv_log_register_print_cb(my_print); /* register print function for debugging */
#endif

    tft.begin();        /* TFT init */
    tft.setRotation(0); /* Landscape orientation */

    lv_disp_buf_init(&disp_buf, buf, NULL, LV_HOR_RES_MAX * 10);

    /*Initialize the display*/
    lv_disp_drv_t disp_drv;
    lv_disp_drv_init(&disp_drv);
    disp_drv.hor_res = LV_HOR_RES_MAX;
    disp_drv.ver_res = LV_VER_RES_MAX;
    disp_drv.flush_cb = my_disp_flush;
    disp_drv.buffer = &disp_buf;
    lv_disp_drv_register(&disp_drv);

    /*Initialize the (dummy) input device driver*/
    lv_indev_drv_t indev_drv;
    lv_indev_drv_init(&indev_drv);
    indev_drv.type = LV_INDEV_TYPE_ENCODER;
    indev_drv.read_cb = read_encoder;
    lv_indev_drv_register(&indev_drv);

    /* Create simple label */
    // user_test_icon();
    setting_screen_title(E_SETTING_FOG);
    // menu_page_init();
    Serial.println("check");
};
uint8_t page_count = 0;
uint16_t test_count;
void loop()
{
    lv_task_handler(); /* let the GUI do its work */
    // set_blink_icon();
    // screen_selected(page_count);
    setting_screen_load_value(0, 0, 0, 1, test_count);
    if (page_count == 0)
        page_count = 1;
    else
        page_count = 0;
    e_buttons_name button = button_process();
    if (button == E_BUTTON_UP)
        test_count = 5;
    else if (button == E_BUTTON_DOWN)
        test_count = 0;
    Serial.println(test_count);
    delay(10);
}

bool status_label_4 = false;
bool status_label_5 = false;
uint8_t count = 0;
void set_blink_icon(void)
{
    set_blink_icon_test(label4, &status_label_4);
    // set_blink_icon_test(label5, &status_label_5);
}

static void set_blink_icon_test(lv_obj_t *obj, bool *status)
{
    if (*status == true)
    {
        lv_obj_set_hidden(obj, 1);
        *status = false;
    }
    else
    {
        lv_obj_set_hidden(obj, 0);
        *status = true;
    }
    char buffer[10];
    sprintf(buffer, "%d", count);
    lv_label_set_text(label4, buffer);
    count++;
}
