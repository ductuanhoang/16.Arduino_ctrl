#include <lvgl.h>
#include "back_free_status.h"
#include "back_selected.h"

lv_obj_t *setting_screen;

LV_IMG_DECLARE(back_free_status);
LV_IMG_DECLARE(back_selected);

void setting_page_init(void)
{
}

void setting_screen_title(uint8_t type_page)
{
    setting_screen = lv_obj_create(NULL, NULL);
    lv_obj_t *label0 = lv_label_create(setting_screen, NULL);
    lv_label_set_long_mode(label0, LV_LABEL_LONG_BREAK); /*Break the long lines*/
    lv_label_set_recolor(label0, true);                  /*Enable re-coloring by commands in the text*/
    lv_label_set_align(label0, LV_LABEL_ALIGN_LEFT);     /*Center aligned lines*/
    switch (type_page)
    {
    case E_SETTING_TEMP:
        lv_label_set_text(label0, "Temp F");
        break;
    case E_SETTING_FOG:
        lv_label_set_text(label0, "Fog %");
        break;
    case E_SETTING_CO2:
        lv_label_set_text(label0, "CO2 ppm");
        break;
    default:
        break;
    }
    lv_obj_set_width(label0, 120);
    lv_obj_align(label0, NULL, LV_ALIGN_IN_TOP_LEFT, 0, 0);

    /*Create an back icon*/
    LV_IMG_DECLARE(back_selected);
    lv_obj_t *img1 = lv_img_create(setting_screen, NULL);
    lv_img_set_src(img1, &back_selected);
    lv_obj_align(img1, NULL, LV_ALIGN_IN_TOP_RIGHT, 0, 0);

    lv_obj_t *label1 = lv_label_create(setting_screen, NULL);
    lv_label_set_long_mode(label1, LV_LABEL_LONG_BREAK); /*Break the long lines*/
    lv_label_set_recolor(label1, true);                  /*Enable re-coloring by commands in the text*/
    lv_label_set_align(label1, LV_LABEL_ALIGN_LEFT);     /*Center aligned lines*/
    lv_label_set_text(label1, "Set");
    lv_obj_set_width(label1, 120);
    lv_obj_align(label1, NULL, LV_ALIGN_IN_TOP_LEFT, 0, 30);

    lv_obj_t *label2 = lv_label_create(setting_screen, NULL);
    lv_label_set_long_mode(label2, LV_LABEL_LONG_BREAK); /*Break the long lines*/
    lv_label_set_recolor(label2, true);                  /*Enable re-coloring by commands in the text*/
    lv_label_set_align(label2, LV_LABEL_ALIGN_LEFT);     /*Center aligned lines*/
    lv_label_set_text(label2, "Up Lag");
    lv_obj_set_width(label2, 120);
    lv_obj_align(label2, NULL, LV_ALIGN_IN_TOP_LEFT, 0, 55);

    lv_obj_t *label3 = lv_label_create(setting_screen, NULL);
    lv_label_set_long_mode(label3, LV_LABEL_LONG_BREAK); /*Break the long lines*/
    lv_label_set_recolor(label3, true);                  /*Enable re-coloring by commands in the text*/
    lv_label_set_align(label3, LV_LABEL_ALIGN_LEFT);     /*Center aligned lines*/
    lv_label_set_text(label3, "Down Lag");
    lv_obj_set_width(label3, 120);
    lv_obj_align(label3, NULL, LV_ALIGN_IN_TOP_LEFT, 0, 80);

    lv_obj_t *label41 = lv_label_create(setting_screen, NULL);
    lv_label_set_long_mode(label41, LV_LABEL_LONG_BREAK); /*Break the long lines*/
    lv_label_set_recolor(label41, true);                  /*Enable re-coloring by commands in the text*/
    lv_label_set_align(label41, LV_LABEL_ALIGN_LEFT);     /*Center aligned lines*/
    lv_label_set_text(label41, "Hi ALR");
    lv_obj_set_width(label41, 120);
    lv_obj_align(label41, NULL, LV_ALIGN_IN_TOP_LEFT, 0, 105);

    lv_obj_t *label51 = lv_label_create(setting_screen, NULL);
    lv_label_set_long_mode(label51, LV_LABEL_LONG_BREAK); /*Break the long lines*/
    lv_label_set_recolor(label51, true);                  /*Enable re-coloring by commands in the text*/
    lv_label_set_align(label51, LV_LABEL_ALIGN_LEFT);     /*Center aligned lines*/
    lv_label_set_text(label51, "Lo ALR");
    lv_obj_set_width(label51, 120);
    lv_obj_align(label51, NULL, LV_ALIGN_IN_TOP_LEFT, 0, 105 + 25);

    setting_screen_value(0, 0, 0, 1, 0);
    lv_scr_load(setting_screen);
}

lv_obj_t *label_set;
lv_obj_t *label_uplag;
lv_obj_t *label_dowlag;
lv_obj_t *label_hi_alr;
lv_obj_t *label_low_alr;

void setting_screen_value(uint16_t set_value, uint16_t uplag_value, uint16_t dowlag_value, uint16_t hi_alr_value, uint16_t lo_alr_value)
{
    label_set = lv_label_create(setting_screen, NULL);
    lv_label_set_long_mode(label_set, LV_LABEL_LONG_BREAK); /*Break the long lines*/
    lv_label_set_recolor(label_set, true);                  /*Enable re-coloring by commands in the text*/
    lv_label_set_align(label_set, LV_LABEL_ALIGN_LEFT);     /*Center aligned lines*/
    lv_label_set_text_fmt(label_set, "%d", set_value);
    lv_obj_set_width(label_set, 120);
    lv_obj_align(label_set, NULL, LV_ALIGN_IN_TOP_LEFT, 90, 30);

    label_uplag = lv_label_create(setting_screen, NULL);
    lv_label_set_long_mode(label_uplag, LV_LABEL_LONG_BREAK); /*Break the long lines*/
    lv_label_set_recolor(label_uplag, true);                  /*Enable re-coloring by commands in the text*/
    lv_label_set_align(label_uplag, LV_LABEL_ALIGN_LEFT);     /*Center aligned lines*/
    lv_label_set_text_fmt(label_uplag, "%d", uplag_value);
    lv_obj_set_width(label_uplag, 120);
    lv_obj_align(label_uplag, NULL, LV_ALIGN_IN_TOP_LEFT, 90, 55);

    label_dowlag = lv_label_create(setting_screen, NULL);
    lv_label_set_long_mode(label_dowlag, LV_LABEL_LONG_BREAK); /*Break the long lines*/
    lv_label_set_recolor(label_dowlag, true);                  /*Enable re-coloring by commands in the text*/
    lv_label_set_align(label_dowlag, LV_LABEL_ALIGN_LEFT);     /*Center aligned lines*/
    lv_label_set_text_fmt(label_dowlag, "%d", dowlag_value);
    lv_obj_set_width(label_dowlag, 120);
    lv_obj_align(label_dowlag, NULL, LV_ALIGN_IN_TOP_LEFT, 90, 80);

    label_hi_alr = lv_label_create(setting_screen, NULL);
    lv_label_set_long_mode(label_hi_alr, LV_LABEL_LONG_BREAK); /*Break the long lines*/
    lv_label_set_recolor(label_hi_alr, true);                  /*Enable re-coloring by commands in the text*/
    lv_label_set_align(label_hi_alr, LV_LABEL_ALIGN_LEFT);     /*Center aligned lines*/
    lv_label_set_text_fmt(label_hi_alr, "%d", hi_alr_value);
    lv_obj_set_width(label_hi_alr, 120);
    lv_obj_align(label_hi_alr, NULL, LV_ALIGN_IN_TOP_LEFT, 70, 105);

    label_low_alr = lv_label_create(setting_screen, NULL);
    lv_label_set_long_mode(label_low_alr, LV_LABEL_LONG_BREAK); /*Break the long lines*/
    lv_label_set_recolor(label_low_alr, true);                  /*Enable re-coloring by commands in the text*/
    lv_label_set_align(label_low_alr, LV_LABEL_ALIGN_LEFT);     /*Center aligned lines*/
    lv_label_set_text_fmt(label_low_alr, "%d", lo_alr_value);
    lv_obj_set_width(label_low_alr, 120);
    lv_obj_align(label_low_alr, NULL, LV_ALIGN_IN_TOP_LEFT, 70, 105 + 25);

    
}

void setting_screen_load_value(uint16_t set_value, uint16_t uplag_value, uint16_t dowlag_value, uint16_t hi_alr_value, uint16_t lo_alr_value)
{
    lv_label_set_text_fmt(label_set, "%d", set_value);
    lv_label_set_text_fmt(label_uplag, "%d", uplag_value);
    lv_label_set_text_fmt(label_dowlag, "%d", dowlag_value);
    lv_label_set_text_fmt(label_hi_alr, "%d", hi_alr_value);
    lv_label_set_text_fmt(label_low_alr, "%d", lo_alr_value);
    lv_scr_load(setting_screen);
}