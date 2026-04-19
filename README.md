# SN
---
WRO documentation
# Introduction
Team Flight is a group of high-school students from Ontario, Canada. This is our second year participating in WRO Future Engineers. We are passionate about robotics and is excited to compete in the open challenge and obstacle challenge for 2026. Our objective is to improve our score and documentation from last year and build a robot using hardware such as a LiDar, Raspberry Pi 5, and new technology introduced to us like the Arduino Nano.

# Our coach
<table>
<tr>
  <td align="center" width="40%">
    <img src="t-photos/coach rice.png" width="100%"/><br>
  </td>

  <td valign="top" width="60%">
 - Head coach of Robotics Competitions, including FLL (First LEGO League),  WRO (World Robotics Olympiad) Robo Sports, Future Engineers, and Robo Mission. Led teams in winning multiple national, international robotics, and programming awards. <br>
  - MSc in Electrical & Computer Engineering from the University of Alberta. <br>
  - BSc in Mathematics from Peking University.<br>
  - Founder of Explorer Robotics, a local robotics club in Ajax and Whitby, teaching coding, AI, robotics, etc.
  </td>
</tr>
</table>

# Team Members
---
<table width="100%" style="border:2px solid #FFC107; border-radius:12px; margin:12px 0;">
  <tr>
    <td width="28%" align="center" style="padding:12px; border-right:6px solid #111;">
    <img 
      alt="Nicole"
      width="190"
      src="t-photos/nicole.jpg"
      style="border-radius: pink 10px" />
    </td>
    <td width="72%" style="padding:12px 16px;">
      <h3 style="margin:0 0 6px 0;">Nicole - nicolejin27@gmail.com</h3>
      <p style="margin-top:8px;">
        <b>About Me:</b> My Name is Nicole, I am 15 years old. I am a figure skater and I also do badminton and track and field for my school. I have been involved in coding and Explorer Robotics since I was 8 and did WRO Future Engineers last year as well.
      </p>
    </td>
  </tr>
</table>

<table width="100%" style="border:2px solid #FFC107; border-radius:12px; margin:12px 0;">
  <tr>
    <td width="28%" align="center" style="padding:12px; border-right:6px solid #111;">
    <img 
      alt="Summer"
      width="190"
      src="t-photos/summer.jpg"
      style="border-radius: pink 10px" />
    </td>
    <td width="72%" style="padding:12px 16px;">
      <h3 style="margin:0 0 6px 0;">Summer - summerlyu@gmail.com</h3>
      <p style="margin-top:8px;">
        <b>About Me:</b> My name is Summer, I am 16 years old. I love figure skating and drawing. I also do badminton, alpine skiing, and track and field for school. I starting coding when I was twelve years old and this is my second year doing WRO Future Engineers. 
      </p>
    </td>
  </tr>
</table>

# Team Photo

<table width="100%" style="border:2px solid #FFC107; border-radius:12px; margin:8px 0;">
  <tr>
    <td align="center" style="padding:14px;">
      <div style="border:2px dashed #FFC107; border-radius:10px; padding:24px; height:320px; display:flex; align-items:center; justify-content:center;">
        <b><img width="1000" height="750" alt="image" src="" /></b>
      </div>
      <div style="margin-top:8px; color:#444;"><em>Team Flight</em></div>
    </td>
  </tr>
</table>

</div>

</br>

---


</br>

# Complete construction manual
The WRO Future Engineers is a competition for self-driven vehicles. Students need to design a model of a car, equip it with electromechanical components, and program it so that it can drive autonomously on the track, avoiding obstacles.
More details about the competition can be found on [the official site of WRO Association](https://wro-association.org/competition/2025-season/#rules).

<img width="700" alt="image" src="MaterialPhoto/fe-map.png" />
The materials are intended to be built with the [Mkdocs](https://www.mkdocs.org/) site generator.

The example of the site is accessible [here](https://world-robot-olympiad-association.github.io/future-engineers-gs/)



# Hardware
---
| Name | Product | Price (CAD)|
| ----------- | ----------- | ----------- |
| RC Car Battery | [`Gens Ace 1300mAh Battery`](https://genstattu.com/gens-ace-1300mah-2s-7-4v-45c-g-tech-lipo-battery-pack-with-deans-plug/?srsltid=AfmBOoo-qPXzcxuH2dIqTfVYg5ghG9WdKi2b53X-R9M8j3XF_JQlLKJL) | $20.60 | 
| Drive Motor | [`Furitek Micro Komodo 1212 3450KV Brushless Motor`](https://furitek.com/products/furitek-micro-komodo-1212-3456kv-brushless-motor-with-15t-steel-pinion-for-fury-wagon-fx118) | $35.00 |
| Servo Motor | [`HS-5055MG 11.9g Metal Gear Digital Micro Servo`](https://hitecrcd.com/hs-5055mg-economy-metal-gear-feather-servo/?srsltid=AfmBOooq_9U4Nehv90Y-tGWqZeo6_1c0_7imuMD9W_dBJmYS1m0sd2Y_) | $25.00 |
| ESC | [`Furitek Lizard Pro 30A/50A ESC`](https://furitek.com/products/combo-of-furitek-lizard-pro-30a-50a-brushed-brushless-esc-for-axial-scx24-with-bluetooth) | $80.00 |
| Camera | [`5MP 1080P HD Camera with OV5647 Sensor`](https://www.amazon.ca/dp/B0D324RKRZ?ref=ppx_yo2ov_dt_b_fed_asin_title) | $35.00 |
| Raspberry Pi 5 8GB | [`Raspberry Pi 5`](https://www.amazon.ca/RasTech-Raspberry-Pi-refroidisseur-inclus/dp/B0DQX6JPVM/ref=sr_1_1_sspa?dib=eyJ2IjoiMSJ9.hjnwoY6Di307ZP-ZXjYU_AmgdoLMC7RS47PGeKtJmhqRtp_k-4b8vYkHuUVwKECxKvsLZj0iaGIogN3I9EAYbOkkLP1mmeFujPf3GbJ2CMFnLyrk19mzn-ImTWQS0CIHPOqaTKx-Ctd1F3jpptYNuSYsMmNl7eHo3YlLS2jAkPG1yBTzWywAtMLtqPDw7h7ECNBYaTd1mWMee3tTjRJN-xMqYHvdCTQPK7nYLTwDF-fwzPk8SNqpdFTZ5PaxoJsqiCrI71GJKbHEhh34FjN7lpqwol6Q_mREib5Uh598Ms4.l7oHUekQqBFhZC9q36eu2RnnsxuvyE01mn0uqJH1tZQ&dib_tag=se&gad_source=1&hvadid=668188233052&hvdev=c&hvexpln=0&hvlocphy=9000756&hvnetw=g&hvocijid=14781734050545810589--&hvqmt=e&hvrand=14781734050545810589&hvtargid=kwd-916491466264&hydadcr=24946_13702398&keywords=raspberry+pi+5+8gb&mcid=370191aac5dd30dfa56c4c13736323b1&qid=1757276490&sr=8-1-spons&sp_csd=d2lkZ2V0TmFtZT1zcF9hdGY&psc=1) | $170.00 |
| Arduino | [`Arduino Nano 33 BLE Rev2`](https://www.digikey.ca/en/products/detail/arduino/ABX00071/22478340) | $33.41 |
| Chassis | [`Gyro Version Drift car 1:24 scale`](https://www.aliexpress.com/item/1005010792530908.html?spm=a2g0o.productlist.main.5.463crzyUrzyUt5&algo_pvid=6c0e6086-1ca4-4045-a5bf-e94f1b148090&algo_exp_id=6c0e6086-1ca4-4045-a5bf-e94f1b148090-6&pdp_ext_f=%7B%22order%22%3A%2218%22%2C%22eval%22%3A%221%22%2C%22fromPage%22%3A%22search%22%7D&pdp_npi=6%40dis%21CAD%21160.71%2173.43%21%21%21806.80%21368.66%21%402103129f17699789369692968ee635%2112000053523542620%21sea%21CA%210%21ABX%211%210%21n_tag%3A-29910%3Bd%3A7a4ca4d%3Bm03_new_user%3A-29895%3BpisId%3A5000000197831940&curPageLogUid=QLqgTPOX4VtS&utparam-url=scene%3Asearch%7Cquery_from%3A%7Cx_object_id%3A1005010792530908%7C_p_origin_prod%3A) | $163.05 | 
| Lidar | [`LDROBOT D500 LiDar Kit`](https://ca.robotshop.com/products/hiwonder-ld19-d500-lidar-developer-kit-360-dtof-laser-scanner-supports-ros1-2-raspberry-pi-jetson-nano?gad_source=1&gad_campaignid=20151193383&gbraid=0AAAAAD_f_xz33tsuMhLsCb4CO_w6kKcep&gclid=EAIaIQobChMI6sqDkubKkgMV1sKfCR2WSxPKEAAYASAAEgIzUfD_BwE) | $149.99 |
| Button | [`Push Switch button 12V 20A Blue LED`](https://www.amazon.ca/dp/B0B96VBFKF/ref=sspa_dk_detail_0?pd_rd_i=B0B96VBFKF&pd_rd_w=jJrLV&content-id=amzn1.sym.516c2169-755e-413a-a38a-68230f4ab66f&pf_rd_p=516c2169-755e-413a-a38a-68230f4ab66f&pf_rd_r=GXSC5RH0ZW4SWHP7KPNV&pd_rd_wg=1JJUB&pd_rd_r=9eb475ae-3436-4910-917b-e7a7d2e68897&sp_csd=d2lkZ2V0TmFtZT1zcF9kZXRhaWw&th=1) | $12.99 |
| Switch | [`DC AC rocker switch`](https://www.amazon.ca/Suitable-125V-250V-Motorcycle-Disconnect-Dispenser/dp/B087PYW9BS) | $5.99 |
| Power regulator | [`Power supply expansion board for raspberry pi 5`](https://ca.robotshop.com/products/yahboom-power-supply-expansion-board-raspberry-pi-5) | $17.54 |

**Total:** 748.57
**With Tax:** 845.88




# Mobility


- [ESC](#ESC)
- [Servo motor](#Servo-motor)
- [Drive motor](#Drive-motor)
- [Power regulator](#Power-regulator)
- [Chassis](#Chassis)
- [Steering and Drive system](#Steering-and-drive-motor)

# Power
- [RC car battery](#RC-car-battery)
- [Ratings and Wiring](#Ratings-and-wiring)

# Sensors and Perception
- [Camera](#Camera)
- [Raspberry pi 5](#Raspberrypi-5)
- [Arduino](#Arduino)
- [LiDar](#LiDar)


# Extra
- [Switch](#Switch)
- [Button](#Button)


# Mobility 

## ESC
<table>
<tr>
  <td valign="top" width="35%">

    
 ### Physical Qualities
  | Field          | Value                              |
  |----------------|------------------------------------|
  | **Product Title** | Furitek Lizard Pro 30A/50A ESC   |
  | **Size**          | 28 × 15.5 mm                     |
  | **Weight**        | 3.7 g                            |
 

  </td>


  <td width="65%" align="center">
    <img width="400" height="400" alt="image" src="MaterialPhoto/ESC.jpg" /><br>
    <em>Furitek Lizard Pro 30A/50A ESC</em>
  </td>
</tr>
</table>

  
### Why we chose this product

We chose Furitek Lizard Pro ESC because it controls the motors speed and ensure that voltage and current is safely delierved to the motor. It's small and manages direction on the open challenge and obstacle challenge. This ESC has a lightweight design, a high capacity and a reliable built-in BEC.


---

### Addtional information
- BIG BEC: **5V or 5V 2.5A**  
- Constant current : **30A**  
- Burst current: **50A**

[click here to return to links](#mobility)

## Servo motor
<table>
<tr>
  <td valign="top" width="35%">

### Physical Qualities
  | Field          | Value                                             |
  |----------------|---------------------------------------------------|
  | **Product Title** | HS-5055MG 11.9g Metal Gear Digital Micro Servo |
  | **Size**          | 0.89 x 0.45 x 0.94 inches                      |
  | **Weight**        | 9.5 grams                                      |
  | **Motor Type**    | 3 Pole Metal Brush Ferrite                     | 
  

  </td>


  <td width="65%" align="center">
    <img width="300" height="300" alt="image" src="MaterialPhoto/Servomotor.jpg" /><br>
    <em>HS-5055MG 11.9g Metal Gear Digital Micro Servo</em>
   </td>
</tr>
</table>

### Why we chose this motor 
We chose the Metal Gear digital Micro Servo because it has metal gears, which can withstand sustained high-speed voltage. It also has plastic casing around it which makes it light. Its compact and gives 1.3 ~ 1.6 kg./cm as maximum torque making it smooth and fast. 

### Additional information
- Operating Voltage Range: **4.8V ~ 6.0V**  
- Speed (Second @ 60°): **0.20 ~ 0.17**  
- Maximum Torque Range oz. / in.: **18 ~ 22**  
- No Load Operating Current draw: **120mA**    

</td>
</tr>
</table>

[click here to return to links](#mobility)


## Drive motor
<table>
<tr>
  <td valign="top" width="35%">

    
 ### Physical Qualities
  | Field          | Value                              |
  |----------------|------------------------------------|
  | **Product Title** | Furitek Micro Komodo 1212 3450KV |
  | **Size**          | 15.5 × 20.6 mm                   |
  | **Weight**        | 17.5 g                           |
  | **Physical State**| Brushless Outrunner (12-slot)    |

  </td>


  <td width="65%" align="center">
    <img width="400" height="400" alt="image" src="MaterialPhoto/DriveMotor.jpg" /><br>
    <em>Furitek Komodo 1212 motor</em>
  </td>
</tr>
</table>


  
### Why we chose this motor 

We chose Furitek Micro Komodo brushless motor because its very compact and light-weight making it easier for our car to manouver. It distrbutes torque smoother and more evenly which helps less cogging and better control. 

---

### Addtional information
- KV: **3450 rpm/V**  
- No-load @10V: **0.7 A**  
- Power: **120 W**  
- Battery: **2–3S LiPo**  
- Resistance: **0.16 Ω**  
- Max Current: **10 A**  
- Slot/Pole: **12**  
- Shaft: **1.5 × 6 mm**

[click here to return to links](#mobility)

## Power regulator
<table>
<tr>
  <td valign="top" width="35%">

    
 ### Physical Qualities
  | Field          | Value                              |
  |----------------|------------------------------------|
  | **Product Title** |  Power supply Expansion board for Raspberry Pi 5  |
  | **Weight**        |      32g                           |
  | **Size**          |      65 by 56mm                 |


  </td>


  <td width="65%" align="center">
    <img width="300" height="300" alt="image" src="MaterialPhoto/PowerRegulator.jpg" /><br>
    <em>Power regulator</em>
  </td>
</tr>
</table>

  
### Why we chose this product
We chose this power supply expansion board because it was tailor made for raspberry-pi. It has many input and output ports and it has efficient voltage stabilization technology, ensuring that the input power supply is stably adjusted for the 5V/5A output, which meets the power needs for the raspberry pi perfectly. Using this power regulator prevents potential low-voltage operation risks and USB interface current limitation. It can also stack directly onto the raspberry pi with screw copper posts, which makes our car more compacts and easier to turn. 
 

---

### Addtional information
- Voltage input: **6~24V**
- Voltage output: **5V/3A (6V Input), 5V/5A (7~24V input)**
-  Output interference: **Type-C, PH2.0-2pin*2, DC5.5*2.1, 2*6pim Bent pin header**
-  Through hole diameter: **M2.5mm**

[click here to return to links](#mobility)

## Chassis
<table>
<tr>
  <td valign="top" width="35%">

    
 ### Physical Qualities
  | Field          | Value                              |
  |----------------|------------------------------------|
  | **Product Title** |    RC Drift Car 1:24 Scale |
  | **Weight**        |      110g                           |
  | **Size**          |       21 x 9.5 x 6 cm               |
 

  </td>


  <td width="65%" align="center">
    <img width="300" height="300" alt="image" src="" /><br>
    <em>  RC Drift Car 1:24 Scale</em>
  </td>
</tr>
</table>

  
### Why we chose this product



---

### Addtional information
- Ranging Distance: **0.03-12m**

[click here to return to links](#mobility)

## Steering and drive motor

[click here to return to links](#mobility)
# Power


## RC car battery
<table>
<tr>
  <td valign="top" width="35%">

  ### Physical Qualities
  | Field | Value |
  |--------|--------|
  | Product Title | Gens Ace 1300mAh 2S 7.4V 25C LiPo |
  | Size | 70.9 × 35.2 × 14.5 mm |
  | Weight | 90 g |
 
  
  </td>

  <td align="center" width="65%">
    <img width="300" height="300" alt="image" src="MaterialPhoto/battery.jpg"/><br>
    <em>Gens Ace 1300mAh 2S LiPo Battery</em>
  </td>
</tr>
</table>

### Why we chose this battery
We chose the Gens Ace Battery because its lightweight and provides a long run time between charges. 
It allows us to keep the self-driving car well balanced which is optimal for the obstacle challenge and open challenge. 
The 7.4V gives good acceleration without noticeable voltage drop and offers stable power delivery without extra wear. 

---


### Additional information
- Voltage: 7.4V  
- Capacity: 1300mAh  
- Discharge Rate: 45C Continuous / 90C Peak  
- Charge Rate: 5C (6.5A Max)  
- Cell Configuration: 2S1P  
- Watt Hours: 9.62Wh  

[click here to return to links](#mobility)

---

##  Ratings and wiring

| Component | Voltage | Normal Current Draw | Max Current Draw | Normal Power | Max Power |
|-|-|-|-|-|-|
| Camera         | 5 V     | 0.16 A   | 0.20 A | 0.80 W  | 1.00 W  |
| Furitek Lizard Pro ESC      | 7.4 V   | 0.007 A  | 0.10 A | 0.05 W  | 0.74 W  |
| Furitek Micro Komodo Motor  | 7.4 V   | 0.95 A   | 10.0 A | 7.00 W  | 74.0 W  |
|  Servo Motor       | 5 V     | 0.10 A   | 0.70 A | 0.50 W  | 3.50 W  |
| MicroSD, LEDs,     | 5 V     | 0.12 A   | 0.30 A | 0.60 W  | 1.50 W  |
| Raspberry Pi 5              | 5 V     | 0.55 A   | 2.00 A | 2.75 W  | 10.0 W  |
| Expansion Board             | 5 V     | 0.12 A   | 0.50 A | 0.60 W  | 2.50 W  |
| Totals                      | —       | —        | —      | ~12.5 W   | ~95 W   |

<br>





[click here to return to links](#mobility)

# Sensors and Perception

## Camera
<table>
<tr>
  <td valign="top" width="35%">

    
 ### Physical Qualities
  | Field          | Value                              |
  |----------------|------------------------------------|
  | **Product Title** | 5/Zero Camera Module (OV5647 Sensor)   |
  | **Cable**         | 15 cm Ribbon Cable                     |
  | **Weight**        | 20 g                                   |
  | **Size**          | 11.6 x 6.6 x 3.7 cm                    |

  </td>


  <td width="65%" align="center">
    <img width="300" height="300" alt="image" src="MaterialPhoto/Camera.jpg" /><br>
    <em>5/Zero Camera Module (OV5647 Sensor)</em>
  </td>
</tr>
</table>

  
### Why we chose this product

We chose the 5/Zero Camera Module because we can use the wide angle camera lens to track the regions of interest and limit the amount of blind spots during the open challenge. It's 175° lens is good for wall detection and true to life colors with automatic light adjustment. It's very compatible with the raspberry pi and easy to install. It can withstand heat up to 70° celcius, making it suitable when we need to use it for longer periods of time. 

---

### Addtional information
- Material: **ABS+ Optimal glass**  
- Lens Pixel : **5MP**  
- Focal Length: **3.6mm**
- Lens Angle: **175°**
- CMOS Size: **1/2.5inch**
- Resolution: **2592x1944**

[click here to return to links](#mobility)
  
  
## Raspberrypi 5
<table>
<tr>
  <td valign="top" width="35%">

    
 ### Physical Qualities
  | Field          | Value                              |
  |----------------|------------------------------------|
  | **Product Title** | RasTech Raspberry Pi 5 Kit (8GB RAM)   |
  | **Weight**        | 70 g                                  |
  | **Size**          | 15 x 9.9 x 3.9 cm                      |
  | **Comes with**    | Pi 5 Board, Case, Active Cooler, Screwdriver |


  </td>


  <td width="65%" align="center">
    <img width="300" height="300" alt="image" src="MaterialPhoto/RaspberryPi5.jpg" /><br>
    <em>RasTech Raspberry Pi 5 Kit (8GB RAM)</em>
  </td>
</tr>
</table>

  
### Why we chose this product

The main part of our robot is the Raspberry Pi 5 and it controls the computer vision and LiDAR data interpretation. It is perfect for energy comsumption and processing power, making it suitable for running our Python codes for the open challenge and obstacle challenge. 

---

### Addtional information
- Manufacturer: **Vemico**  
- Wireless : **802.11ac Wi-Fi, Bluetooth**  
- Processor: **Broadcome BCM2712, Quad-Core Cortex-A76 @ 2.4 GHz**
- RAM: **8 GB LPDDR4X-4266**
- GPU: **VideoCore VII (Integrated)**
- Storage: **microSD**
- Ports: **2x USB 3.0, 2x USB 2.0, 2x micro HDMI, Ethernet, GPIO**
- OS: **Raspberry Pi OS**

[click here to return to links](#mobility)
  
## Arduino

 


## LiDar
<table>
<tr>
  <td valign="top" width="35%">

    
 ### Physical Qualities
  | Field          | Value                              |
  |----------------|------------------------------------|
  | **Product Title** | LDROBOT D500 LiDAR   |
  | **Weight**        | 45 g                                  |
  | **Size**          | 54 × 46.3 × 35 mm                     |
 

  </td>


  <td width="65%" align="center">
    <img width="300" height="300" alt="image" src="MaterialPhoto/LiDar.jpg" /><br>
    <em>LDROBOT D500 LiDAR </em>
  </td>
</tr>
</table>

  
### Why we chose this product

 We are going to use the LDROBOT D500 LiDAR for obstacle challenge because it provides accurate range data in every direction up to 12 meters. We are also switching to use the LiDAR instead of the camera because it doesn't depend of good lighting to function properly. With its long scanning range, it can detect obstacles further away and then turn accordingly. 

---

### Addtional information
- Ranging Distance: **0.03-12m**  
- Accuracy : **±10 mm (0.3–0.5 m), ±20 mm (0.5–2 m), ±30 mm (2–12 m)**  
- Scanning Angle: **360°**
- Scanning frequency: **6-13 Hz**
- Ranging frequency: **5000Hz**
- Wavelength: **895 – 915 nm (Typ. 905 nm)**
- Interface: **UART @ 230400 baud**
- Ambient Light Tolerance: **up to 60k Lux**
- Power Supply: **5V**
- Power Comsumption: **1.45W (290 mA)**
- Operating Temp: **-10° to 45° C**

[click here to return to links](#mobility)

# Extra
  
## Button

[click here to return to links](#mobility)
## Switch
<table>
<tr>
  <td valign="top" width="35%">

 | Field          | Value                              |
  |----------------|------------------------------------|
  | **Product Title** |  DC AC rocker switch  |
  | **Weight**        |        4g                    |
  | **Size**          |    1.1cm by 2.1cm by 1.5cm      |
  |**Brand**          |  	EKYLIN   |
  |**Material**       | Metal, plastic  |


  </td>


  <td width="65%" align="center">
    <img width="300" height="300" alt="image" src="MaterialPhoto/Switch.jpg" /><br>
    <em>DC AC rocker switch</em>
  </td>
</tr>
</table>

  
### Why we chose this product
We choose this switch because it was simple and easy to install. This switch is suitable for AC 125V 10A, AC 250V 6A, DC 12V 20A, DC 24V 10A, DC 36V 6.5A. It was made by an insulated plastic and copper pins, with a mechanical life of more than 8 thousand cycles and an electrical life of more than 10 thousand. The high operating temperature allows it to still work and function properly when it is used for an extended period of time. 
 

---

### Addtional information
- Current rating: **10 amps**
- Operating voltage:**125 Volts (AC)**
- Insulation resistance: **100MΩ min**
- Operating temperature: **-25°C~85°C**

[click here to return to links](#mobility)

  



# Tools and Equipment
| Name | Product | Price (CAD)|
| ----------- | ----------- | ----------- |
| 3D Printer | [`Bambu Lab X1 Carbon 3D Printer`](https://genstattu.com/gens-ace-1300mah-2s-7-4v-45c-g-tech-lipo-battery-pack-with-deans-plug/?srsltid=AfmBOoo-qPXzcxuH2dIqTfVYg5ghG9WdKi2b53X-R9M8j3XF_JQlLKJL) | $1289 | 
| Soldering Kit| [`TOAUTO DS90 Soldering Station`](https://www.amazon.ca/FASTTOBUY-Soldering-Station-194%C2%B0F-896%C2%B0F-Temperature/dp/B082HP4513?source=ps-sl-shoppingads-lpcontext&ref_=fplfs&smid=A1QHHBFTGR8LSC&th=1) | $90 |
| Screws, Screwdriver, Pliers, etc. | n/a | $~35 |  
| Fillament 1kg | [`EconoFil™ Standard PLA Filament`](https://www.inksmith.ca/collections/filament/products/econofil-standard-pla-filament-black-1-75mm-1-kg?variant=50056253276442) | $26 |  

**Total:** $~1440 *No Tax*

**With Tax:** $~1627.2

# 3D design and fabrication

| *Component that holds the raspberry pi, arduino and power regulator* |
| <img src="models/raspi.stl">  |
| *Component that holds the camera up*|
| <img src=""> |

### Overview
- a main part of our project was the 3D print which allowed us to design and refine custom parts of our chassis for best results
- Our 3D print held major components to the function of our robot like the arduino, raspberry pi, power regulator, camera, and liDar.
- Fabrication in Onshape, printing using Prusa MK4 with PLA filament

### Printing information

| Setting | Value |
|----------|--------|
| Printer | [`Prusa MK4`](https://www.prusa3d.com/product/original-prusa-mk4s/?utm_source=google&utm_medium=cpc&utm_campaign=EN-CA_Search_Text_Brand&utm_id=804628075&gad_source=1&gad_campaignid=804628075&gbraid=0AAAAADkiZoOd65faDM0bHRhBQj7ky7NcF&gclid=CjwKCAjwhe3OBhABEiwA6392zNFtJI5Mq8r8JDHuuQUJW8VSS6PgJko4EIIhgfwNkfE0DJi9G7rwxBoCjJwQAvD_BwE) |
| Material | PLA |
| Nozzle Temperature | 230 °C |
| Bed Temperature | 65 °C (Textured PEI Plate) |
| Filament Diameter | 1.75 mm |
| Flow Ratio | 0.96 |
| Max Volumetric Speed | 12 mm³/s |
| Layer Height | 0.2 mm |
| Nozzle Diameter | 0.4 mm |
| Infill Density | 15 % |

We chose PLA because of it's easy accessibility and affordable cost, allowing quick iteration without sacrificing accuracy. It's proformance is reliable, and it is easy to print again if there was a mistake. 

### Photo gallery 
<table>
  <tr>
    <td align="center" style="border:1px solid #ddd; padding:15px;">
    <img width="563" height="750" alt="image" src="" /><br/>
      <em><strong>Front View </strong></em>
    </td>
    <td align="center" style="border:1px solid #ddd; padding:15px;">
      <img width="563" height="750" alt="image" src="" /><br/>
      <em><strong>Back view</strong></em>
    </td>
    <td align="center" style="border:1px solid #ddd; padding:15px;">
     <img width="563" height="750" alt="image" src="" /><br/>
      <em><strong>Top View</strong></em>
    </td>
  </tr>
  <tr>
    <td align="center" style="border:1px solid #ddd; padding:15px;">
     <img width="563" height="750" alt="image" src="" /><br/>
      <em><strong>Left Side View</strong></em>
    </td>
    <td align="center" style="border:1px solid #ddd; padding:15px;">
      <img width="563" height="750" alt="image" src="" /><br/>
      <em><strong>Right Side View</strong></em>
    </td>
    <td align="center" style="border:1px solid #ddd; padding:15px;">
      <img width="563" height="750" alt="image" src="" /><br/>
      <em><strong>Bottom View</strong></em>
    </td>
  </tr>
</table>
<br>
---







  

