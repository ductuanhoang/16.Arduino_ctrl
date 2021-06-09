1. Coppy all folder and file in "user_lib" to C:\Users\<Your name PC>\Documents\Arduino\libraries"
2. Connect TFT LCD with esp32 follow
#define TFT_MOSI 23  //In some display driver board, it might be written as "SDA" and so on.
#define TFT_SCLK 18 
#define TFT_CS 5     //Chip select control pin
#define TFT_DC 15     // Data Command control pin
#define TFT_RST 16   // Reset pin (could connect to Arduino RESET pin)

3. Link for download icon "https://www.flaticon.com/search?word=mute&fbclid=IwAR2a7o7v5gA1kqWeK91ck2F0RNM0JUnR5TCo8Wakz-d1idIEHfGAmRqipVk"
3.1 this project use lvgl lib so you can using "https://lvgl.io/tools/imageconverter" to convert icon image to array


4. connect button with GPIO34

