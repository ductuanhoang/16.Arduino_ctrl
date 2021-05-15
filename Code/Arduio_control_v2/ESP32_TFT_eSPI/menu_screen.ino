#include <lvgl.h>
#include "fan_icon_display.h"

lv_obj_t *menu_screen;

lv_obj_t *menu_label_fan_cycle;
lv_obj_t *menu_label_temp;
lv_obj_t *menu_label_humi;
lv_obj_t *menu_label_fan_ctrl;

void menu_page_init(void)
{
    menu_screen = lv_obj_create(NULL, NULL);
    lv_obj_t *label0 = lv_label_create(menu_screen, NULL);
    lv_label_set_long_mode(label0, LV_LABEL_LONG_BREAK); /*Break the long lines*/
    lv_label_set_recolor(label0, true);                  /*Enable re-coloring by commands in the text*/
    lv_label_set_align(label0, LV_LABEL_ALIGN_LEFT);     /*Center aligned lines*/
    lv_label_set_text(label0, "Menu");
    lv_obj_set_width(label0, 120);
    lv_obj_align(label0, NULL, LV_ALIGN_IN_TOP_LEFT, 0, 0);

    /*Create an back icon*/
    LV_IMG_DECLARE(back_selected);
    lv_obj_t *img1 = lv_img_create(menu_screen, NULL);
    lv_img_set_src(img1, &back_selected);
    lv_obj_align(img1, NULL, LV_ALIGN_IN_TOP_RIGHT, 0, 0);

    /* icon label create*/
    /*Create an fan icon*/
    LV_IMG_DECLARE(fan_icon_display);
    lv_obj_t *img2 = lv_img_create(menu_screen, NULL);
    lv_img_set_src(img2, &fan_icon_display);
    lv_obj_align(img2, NULL, LV_ALIGN_IN_TOP_LEFT, 10, 40);

    LV_IMG_DECLARE(temperature_f);
    lv_obj_t *img3 = lv_img_create(menu_screen, NULL);
    lv_img_set_src(img3, &temperature_f);
    lv_obj_align(img3, NULL, LV_ALIGN_IN_TOP_LEFT, 10, 70);

    LV_IMG_DECLARE(humidity_icon);
    lv_obj_t *img4 = lv_img_create(menu_screen, NULL);
    lv_img_set_src(img4, &humidity_icon);
    lv_obj_align(img4, NULL, LV_ALIGN_IN_TOP_LEFT, 10, 100);

    LV_IMG_DECLARE(fan_icon_display);
    lv_obj_t *img5 = lv_img_create(menu_screen, NULL);
    lv_img_set_src(img5, &fan_icon_display);
    lv_obj_align(img5, NULL, LV_ALIGN_IN_TOP_LEFT, 10, 130);

    setting_menu_value();
    lv_scr_load(menu_screen);
}

void setting_menu_value()
{
    menu_label_fan_cycle = lv_label_create(menu_screen, NULL);
    lv_label_set_long_mode(menu_label_fan_cycle, LV_LABEL_LONG_BREAK); /*Break the long lines*/
    lv_label_set_recolor(menu_label_fan_cycle, true);                  /*Enable re-coloring by commands in the text*/
    lv_label_set_align(menu_label_fan_cycle, LV_LABEL_ALIGN_LEFT);     /*Center aligned lines*/
    lv_label_set_text(menu_label_fan_cycle, "Cycle");
    lv_obj_set_width(menu_label_fan_cycle, 120);
    lv_obj_align(menu_label_fan_cycle, NULL, LV_ALIGN_IN_TOP_LEFT, 70, 40);

    menu_label_temp = lv_label_create(menu_screen, NULL);
    lv_label_set_long_mode(menu_label_temp, LV_LABEL_LONG_BREAK); /*Break the long lines*/
    lv_label_set_recolor(menu_label_temp, true);                  /*Enable re-coloring by commands in the text*/
    lv_label_set_align(menu_label_temp, LV_LABEL_ALIGN_LEFT);     /*Center aligned lines*/
    lv_label_set_text(menu_label_temp, "AUTO");
    lv_obj_set_width(menu_label_temp, 120);
    lv_obj_align(menu_label_temp, NULL, LV_ALIGN_IN_TOP_LEFT, 70, 70);

    menu_label_humi = lv_label_create(menu_screen, NULL);
    lv_label_set_long_mode(menu_label_humi, LV_LABEL_LONG_BREAK); /*Break the long lines*/
    lv_label_set_recolor(menu_label_humi, true);                  /*Enable re-coloring by commands in the text*/
    lv_label_set_align(menu_label_humi, LV_LABEL_ALIGN_LEFT);     /*Center aligned lines*/
    lv_label_set_text(menu_label_humi, "ON");
    lv_obj_set_width(menu_label_humi, 120);
    lv_obj_align(menu_label_humi, NULL, LV_ALIGN_IN_TOP_LEFT, 70, 100);

    menu_label_fan_ctrl = lv_label_create(menu_screen, NULL);
    lv_label_set_long_mode(menu_label_fan_ctrl, LV_LABEL_LONG_BREAK); /*Break the long lines*/
    lv_label_set_recolor(menu_label_fan_ctrl, true);                  /*Enable re-coloring by commands in the text*/
    lv_label_set_align(menu_label_fan_ctrl, LV_LABEL_ALIGN_LEFT);     /*Center aligned lines*/
    lv_label_set_text(menu_label_fan_ctrl, "ON");
    lv_obj_set_width(menu_label_fan_ctrl, 120);
    lv_obj_align(menu_label_fan_ctrl, NULL, LV_ALIGN_IN_TOP_LEFT, 70, 130);
}