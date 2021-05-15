#include <lvgl.h>
static void page_1(void);
static void page_2(void);

lv_obj_t *screen1;
lv_obj_t *screen2;
void screen_init(void)
{
    page_1();
    page_2();
}
void screen_selected(uint8_t page_number)
{
    if (page_number == 1)
    {
        lv_scr_load(screen1);
    }
    else
    {
        lv_scr_load(screen2);
    }
}

static void page_1(void)
{
    screen1 = lv_obj_create(NULL, NULL);
    LV_IMG_DECLARE(setting_icon);
    LV_IMG_DECLARE(setting_icon_blue);

    LV_IMG_DECLARE(menu);
    LV_IMG_DECLARE(menu_select);

    LV_IMG_DECLARE(volume_run);
    LV_IMG_DECLARE(volume_mute);
    /*Darken the button when pressed*/
    static lv_style_t style;
    lv_style_init(&style);
    lv_style_set_image_recolor_opa(&style, LV_STATE_PRESSED, LV_OPA_30);
    lv_style_set_image_recolor(&style, LV_STATE_PRESSED, LV_COLOR_BLACK);
    lv_style_set_text_color(&style, LV_STATE_DEFAULT, LV_COLOR_WHITE);

    /*Create an Image button*/
    imgbtn1 = lv_imgbtn_create(screen1, NULL);
    lv_imgbtn_set_src(imgbtn1, LV_BTN_STATE_RELEASED, &setting_icon);
    lv_imgbtn_set_src(imgbtn1, LV_BTN_STATE_PRESSED, &setting_icon);
    lv_imgbtn_set_src(imgbtn1, LV_BTN_STATE_CHECKED_RELEASED, &setting_icon);
    lv_imgbtn_set_src(imgbtn1, LV_BTN_STATE_CHECKED_PRESSED, &setting_icon);
    lv_imgbtn_set_checkable(imgbtn1, true);
    lv_obj_add_style(imgbtn1, LV_IMGBTN_PART_MAIN, &style);
    lv_obj_align(imgbtn1, NULL, LV_ALIGN_IN_TOP_MID, 0, 0);

    /*Create an Image button*/
    lv_obj_t *imgbtn2 = lv_imgbtn_create(screen1, NULL);
    lv_imgbtn_set_src(imgbtn2, LV_BTN_STATE_RELEASED, &menu);
    lv_imgbtn_set_src(imgbtn2, LV_BTN_STATE_PRESSED, &menu);
    lv_imgbtn_set_src(imgbtn2, LV_BTN_STATE_CHECKED_RELEASED, &menu_select);
    lv_imgbtn_set_src(imgbtn2, LV_BTN_STATE_CHECKED_PRESSED, &menu_select);
    lv_imgbtn_set_checkable(imgbtn2, true);
    lv_obj_add_style(imgbtn2, LV_IMGBTN_PART_MAIN, &style);
    lv_obj_align(imgbtn2, NULL, LV_ALIGN_IN_TOP_LEFT, 0, 0);

    /*Create an Image button*/
    lv_obj_t *imgbtn3 = lv_imgbtn_create(screen1, NULL);
    lv_imgbtn_set_src(imgbtn3, LV_BTN_STATE_RELEASED, &volume_run);
    lv_imgbtn_set_src(imgbtn3, LV_BTN_STATE_PRESSED, &volume_run);
    lv_imgbtn_set_src(imgbtn3, LV_BTN_STATE_CHECKED_RELEASED, &volume_mute);
    lv_imgbtn_set_src(imgbtn3, LV_BTN_STATE_CHECKED_PRESSED, &volume_mute);
    lv_imgbtn_set_checkable(imgbtn3, true);
    lv_obj_add_style(imgbtn3, LV_IMGBTN_PART_MAIN, &style);
    lv_obj_align(imgbtn3, NULL, LV_ALIGN_IN_TOP_RIGHT, 0, 0);

    /*Create an humidity icon*/
    LV_IMG_DECLARE(humidity_icon);
    lv_obj_t *img1 = lv_img_create(screen1, NULL);
    lv_img_set_src(img1, &humidity_icon);
    lv_obj_align(img1, NULL, LV_ALIGN_IN_TOP_LEFT, 0, 40);

    LV_IMG_DECLARE(temperature_f);
    lv_obj_t *img2 = lv_img_create(screen1, NULL);
    lv_img_set_src(img2, &temperature_f);
    lv_obj_align(img2, NULL, LV_ALIGN_IN_TOP_LEFT, 0, 70);

    LV_IMG_DECLARE(co2_icon);
    lv_obj_t *img3 = lv_img_create(screen1, NULL);
    lv_img_set_src(img3, &co2_icon);
    lv_obj_align(img3, NULL, LV_ALIGN_IN_TOP_LEFT, 0, 100);

    LV_IMG_DECLARE(fan_icon_blue);
    lv_obj_t *img4 = lv_img_create(screen1, NULL);
    lv_img_set_src(img4, &fan_icon_blue);
    lv_obj_align(img4, NULL, LV_ALIGN_IN_BOTTOM_LEFT, 0, 0);

    LV_IMG_DECLARE(heater_on);
    lv_obj_t *img5 = lv_img_create(screen1, NULL);
    lv_img_set_src(img5, &heater_on);
    lv_obj_align(img5, NULL, LV_ALIGN_IN_BOTTOM_MID, 0, 0);

    LV_IMG_DECLARE(fog_on);
    lv_obj_t *img6 = lv_img_create(screen1, NULL);
    lv_img_set_src(img6, &fog_on);
    lv_obj_align(img6, NULL, LV_ALIGN_IN_BOTTOM_RIGHT, 0, 0);

    // set text humidity
    lv_obj_t *label1 = lv_label_create(screen1, NULL);
    lv_label_set_long_mode(label1, LV_LABEL_LONG_BREAK); /*Break the long lines*/
    lv_label_set_recolor(label1, true);                  /*Enable re-coloring by commands in the text*/
    lv_label_set_align(label1, LV_LABEL_ALIGN_LEFT);     /*Center aligned lines*/
    lv_label_set_text(label1, "10.5");
    lv_obj_set_width(label1, 120);
    lv_obj_align(label1, NULL, LV_ALIGN_IN_TOP_LEFT, 40, 40);
    //
    lv_obj_t *label2 = lv_label_create(screen1, NULL);
    lv_label_set_long_mode(label2, LV_LABEL_LONG_BREAK); /*Break the long lines*/
    lv_label_set_recolor(label2, true);                  /*Enable re-coloring by commands in the text*/
    lv_label_set_align(label2, LV_LABEL_ALIGN_LEFT);     /*Center aligned lines*/
    lv_label_set_text(label2, "21.5");
    lv_obj_set_width(label2, 120);
    lv_obj_align(label2, NULL, LV_ALIGN_IN_TOP_LEFT, 40, 70);
    // CO2
    lv_obj_t *label3 = lv_label_create(screen1, NULL);
    lv_label_set_long_mode(label3, LV_LABEL_LONG_BREAK); /*Break the long lines*/
    lv_label_set_recolor(label3, true);                  /*Enable re-coloring by commands in the text*/
    lv_label_set_align(label3, LV_LABEL_ALIGN_LEFT);     /*Center aligned lines*/
    lv_label_set_text(label3, "500");
    lv_obj_set_width(label3, 120);
    lv_obj_align(label3, NULL, LV_ALIGN_IN_TOP_LEFT, 40, 100);

    // set text humidity
    label4 = lv_label_create(screen1, NULL);
    lv_label_set_long_mode(label4, LV_LABEL_LONG_BREAK); /*Break the long lines*/
    lv_label_set_recolor(label4, true);                  /*Enable re-coloring by commands in the text*/
    lv_label_set_align(label4, LV_LABEL_ALIGN_LEFT);     /*Center aligned lines*/
    lv_label_set_text(label4, "10.5");
    lv_obj_set_width(label4, 120);
    lv_obj_align(label4, NULL, LV_ALIGN_IN_TOP_LEFT, 80, 40);

    label5 = lv_label_create(screen1, NULL);
    lv_label_set_long_mode(label5, LV_LABEL_LONG_BREAK); /*Break the long lines*/
    lv_label_set_recolor(label5, true);                  /*Enable re-coloring by commands in the text*/
    lv_label_set_align(label5, LV_LABEL_ALIGN_LEFT);     /*Center aligned lines*/
    lv_label_set_text(label5, "21.5");
    lv_obj_set_width(label5, 120);
    lv_obj_align(label5, NULL, LV_ALIGN_IN_TOP_LEFT, 80, 70);
    // CO2
    lv_obj_t *label6 = lv_label_create(screen1, NULL);
    lv_label_set_long_mode(label6, LV_LABEL_LONG_BREAK); /*Break the long lines*/
    lv_label_set_recolor(label6, true);                  /*Enable re-coloring by commands in the text*/
    lv_label_set_align(label6, LV_LABEL_ALIGN_LEFT);     /*Center aligned lines*/
    lv_label_set_text(label6, "500.5");
    lv_obj_set_width(label6, 120);
    lv_obj_align(label6, NULL, LV_ALIGN_IN_TOP_LEFT, 80, 100);
}

static void page_2(void)
{
    screen2 = lv_obj_create(NULL, NULL);
    lv_obj_t *label8 = lv_label_create(screen2, NULL);
    lv_label_set_long_mode(label8, LV_LABEL_LONG_BREAK); /*Break the long lines*/
    lv_label_set_recolor(label8, true);                  /*Enable re-coloring by commands in the text*/
    lv_label_set_align(label8, LV_LABEL_ALIGN_LEFT);     /*Center aligned lines*/
    lv_label_set_text(label8, "tuan test page 2");
    lv_obj_set_width(label8, 120);
    lv_obj_align(label8, NULL, LV_ALIGN_IN_TOP_LEFT, 80, 40);
}
