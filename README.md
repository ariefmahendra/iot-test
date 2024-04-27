## Program IoT
### Schematic dengan sensor LDR
1. [schematic](1_SCHEMATIC/Schematic.svg)
2. [desain PCB](1_SCHEMATIC/PCB.svg)
3. 3D Model
   1. [Tampak Depan](1_SCHEMATIC/tampak-depan.png)
   2. [Tampak Belakang](1_SCHEMATIC/tampak-belakang.png)

### Komunikasi serial antara pyhton dengan Arduino (boudrate = 9600)
1. [Program arduino (Sebagai Receiver)](2_SERIAL_COMMUNICATION/receiver.ino)
2. [Program python (Sebagai Sender)](2_SERIAL_COMMUNICATION/sender.py)

### Komunikasi IOT dari mikrokontroller ESP32 sebagai publisher dan python sebagai serverside subscriber

Data yang telah di subscribe sesuai topik akan disimpan langsung ke mysql, sehinnga [DDL](3_MQTT_PUB_SUB/DDL.sql) dapat disesuaikan.

1. [Program Publisher (Menggunakan micropython)](3_MQTT_PUB_SUB/pub.py)
2. [Program Subscriber (Script python)](3_MQTT_PUB_SUB/sub.py)

