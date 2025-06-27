---

# Rovello – UAB 2025

Un projecte de robòtica fet per a automatitzar el procés de torrat de pa amb visió per computador, control de motors i dispensació d’oli.

---

## Què fa aquest robot?

Aquest sistema agafa una llesca de pa, la mou sota una càmera per analitzar el grau de torrat i, si el pa està correctament torrat, el porta a una zona on se li afegeix oli mitjançant un solenoide. Finalment, el pa és traslladat fins al plat.

---

## Mòduls del sistema

* **main.py** – Arxiu principal que executa tot el procés.
* **system\_manager.py** – Controlador principal que coordina visió, motors i oli.
* **vision\_module.py** – Captura imatges i calcula el grau de torrat.
* **actuator\_control.py** – Control del motor de la cinta transportadora.
* **oil\_dispenser\_control.py** – Control del solenoide d’oli.
* **toasting\_module.py** – Lògica de decisió basada en el torrat.
* **config\_module.py** – Paràmetres configurables del sistema.

---

## Hardware utilitzat

* Raspberry Pi Zero
* Càmera Raspberry Pi (Picamera2)
* Font d'alimentació ATX 12V DC-DC
* Solenoide DC 12V
* Relé mecànic
* Motor DC 12V
* Controladora de motor IBT-2
* LED indicador

---

## Com ajustar els paràmetres

Els paràmetres estan definits a `config_module.py`. Pots editar-los segons el comportament del sistema:

```python
self.toasting_level  = 0.35   # Llindar per considerar el pa torrat
self.cam_time        = 1.0    # Temps per moure el pa sota la càmera
self.oil_time        = 1.5    # Temps per moure el pa a la zona d'oli
self.plate_time      = 2.0    # Temps per moure el pa fins al plat
self.oil_active_time = 1.0    # Temps d'activació del solenoide d'oli
```

---

## Com executar-ho

1. Connecta't a la Raspberry Pi per SSH:

   ```bash
   ssh pi@raspberrypi.local
   ```

2. Navega al directori del projecte:

   ```bash
   cd /home/pi/Prova/Projecte_rovello
   ```

3. Executa el programa principal:

   ```bash
   python3 main.py
   ```

---

## 📂 Estructura de carpetes

```
Projecte_rovello/
├── actuator_control.py
├── config_module.py
├── main.py
├── oil_dispenser_control.py
├── system_manager.py
├── toasting_module.py
├── vision_module.py
└── imatges/
```
## Video explicatiu

https://drive.google.com/file/d/1s0li1pyr3_-Z9FdZ7bmrCi1DlDDNkcoP/view?usp=sharing

## Autors

Pere Llauradó Adeva
Marçal Armengol Romero
Gerard Purtí Ramirez
Jordi Viera Antequera

Universitat Autonoma de Barcelona Facultat d'Enginyeria
