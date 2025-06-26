# Rovelló – Robot Automatitzat per Torrar Pa i Dispensar Oli

Aquest projecte controla un sistema automàtic que:
1. Mou una llesca de pa sota una càmera.
2. Avalua si està prou torrada mitjançant visió per computador.
3. Dispença oli mitjançant un solenoide.
4. Finalitza portant la llesca fins al plat.

---

## Estructura del projecte

- `main.py`  
  Punt d'entrada. Només crea i executa el `SystemManager`.

- `system_manager.py`  
  Coordinador principal. Gestiona el flux: moure cinta → analitzar → oli → plat.

- `vision_module.py`  
  Captura imatges i calcula el grau de torrat analitzant la lluminositat del pa. Utilitza la càmera Pi (`picamera2`) i OpenCV per identificar la peça de pa i mesurar com de torrada està.

- `actuator_control.py`  
  Control del motor de la cinta amb dos pins PWM (direcció i velocitat).

- `oil_dispenser_control.py`  
  Activa el solenoide que dispença oli durant un temps configurat.

- `config_module.py`  
  Conté tots els paràmetres editables del sistema: nivell de torrat, temps de moviment, durada de l'oli, etc.

- `toasting_module.py`  
  (Opcional / no utilitzat) Conté una altra aproximació per avaluar el nivell de torrat, però no està integrat.

---

## Funcionament de la visió per computador

1. Es captura una imatge amb la càmera Pi.
2. Es converteix a espai de color HSV.
3. Es detecta primer la cinta blava i després es busca una forma quadrada (la llesca).
4. Es calcula el grau de torrat a partir del canal de lluminositat (V):
   - Torrat = `1.0 - (lluminositat mitjana / 255)`
   - El valor resultant és entre `0.0` (pa molt clar) i `1.0` (molt torrat).
5. Si el valor supera el llindar definit a `config_module.py`, el pa és considerat **torrat**.

---

## ⚙️ Com ajustar els paràmetres

Els paràmetres estan definits a `config_module.py`. Pots editar-los segons el comportament del sistema:

```python
self.toasting_level  = 0.35   # Llindar per considerar el pa torrat
self.cam_time        = 1.0    # Temps per moure el pa sota la càmera
self.oil_time        = 1.5    # Temps per moure el pa a la zona d'oli
self.plate_time      = 2.0    # Temps per moure el pa fins al plat
self.oil_active_time = 1.0    # Temps d'activació del solenoide d'oli
