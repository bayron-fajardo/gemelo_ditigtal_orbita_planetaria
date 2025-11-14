# Simulador del Sistema Solar - En camino a un Gemelo Digital

Este proyecto de simulación del sistema solar,basado en física real. 
Actualmente reproduce el movimiento de los planetas y compara los resultados con datos de referencia aproximados tomados de fuentes de la NASA.

Este proyecto no es todavía un gemelo digital completo, sino una simulación con enfoque hacia el concepto de gemelo digital. La diferencia principal es que una simulación reproduce el comportamiento de un sistema con modelos matemáticos, mientras que un gemelo digital utiliza datos reales en tiempo real para mantener sincronización con el sistema físico.
La idea es que, en el futuro, este proyecto se conecte a una API astronómica real (como NASA Horizons) para actualizar posiciones y realizar predicciones precisas, momento en el que podría considerarse un gemelo digital funcional.

## ¿Qué hace este programa?

Es una simulación visual donde puedes ver:
- Los planetas moviéndose alrededor del Sol
- Sus órbitas (esas líneas que van dejando)
- Qué tan preciso es el modelo comparado con la "realidad"
- Información detallada de cada planeta cuando lo seleccionas

El concepto de gemelo digital se aplica aquí al tener dos representaciones del sistema:
1. La simulación física (calculada por el programa).
2. Los datos “reales” de referencia (aproximaciones tomadas como si vinieran de la NASA).
Esto permite analizar la precisión del modelo y establecer la base de comparación que caracteriza a los gemelos digitales.

## Instalación

### Requisitos previos
- Python 3.7 o superior (yo uso 3.10)
- pip (el gestor de paquetes de Python)

### Pasos para instalar

1. **Clona o descarga el proyecto**
   ```bash
   git clone [url-del-repo]
   cd sistema-solar
   ```
   O simplemente descarga los archivos y ponlos en una carpeta.

2. **Instala pygame**
   ```bash
   pip install -r requirements.txt
   ```
   
   Si te da problemas, prueba con:
   ```bash
   pip install pygame
   ```

3. **Ejecuta el programa**
   ```bash
   python app.py
   ```

Se abrirá una ventana con la simulación.

## Controles

Una vez que esté corriendo, puedes usar:

- **ESPACIO**: Pausar o reanudar la simulación
- **S**: Re-sincronizar con los datos de NASA (resetea todo)
- **T**: Limpiar las trayectorias (borra las líneas de las órbitas)
- **Click izquierdo**: Seleccionar un planeta para ver su info
- **Flecha ARRIBA**: Acelerar el tiempo
- **Flecha ABAJO**: Ralentizar el tiempo

## ¿Cómo funciona? (Explicación de las funciones principales)

### Clase `Planet`

Esta es la clase más importante, representa cada planeta/estrella:

**`__init__`**: Constructor básico. Aquí se inicializan todas las propiedades del planeta como su posición, masa, color, etc. También tiene variables para el "gemelo digital" como `real_x` y `real_y` que son la posición "real" según NASA.

**`screen_pos()` y `real_screen_pos()`**: Convierten las coordenadas del espacio (que están en metros) a píxeles en la pantalla. Básicamente hacen que los planetas se vean donde deben en la ventana.

**`calculate_deviation()`**: Calcula qué tan lejos está la simulación de la "realidad". Usa el teorema de Pitágoras para medir la distancia entre donde el modelo dice que está el planeta vs donde "realmente" está.

**`draw()`**: Dibuja el planeta en la pantalla. También dibuja:
- Las órbitas (líneas de colores)
- La posición real (círculo verde)
- Una línea que conecta simulación con realidad
- Indicadores de precisión (✓ o ⚠)

**`attraction()`**: Esta es la parte física importante. Calcula la fuerza gravitacional entre dos cuerpos usando la Ley de Gravitación Universal de Newton (esa famosa: F = G*m1*m2/r²). Devuelve la fuerza en X e Y.

**`update_position()`**: Aquí pasa la magia. Calcula todas las fuerzas que actúan sobre el planeta, actualiza su velocidad y luego su posición. Básicamente simula el movimiento usando física real.

### Función `load_nasa_data()`

Simula la carga de datos de NASA. En un proyecto real esto haría una petición HTTP a la API de NASA, pero aquí solo devuelve datos hardcodeados que son aproximadamente correctos para noviembre 2025.

Devuelve un diccionario con:
- Posiciones iniciales (en UA - Unidades Astronómicas)
- Velocidades iniciales (en km/s)
- Masas, colores, tamaños, etc.

### Función `sync_planets_with_nasa()`

Toma los datos del formato de NASA y los convierte en objetos `Planet` que podemos usar en la simulación. Es básicamente un "traductor" entre el formato de datos y nuestras clases.

### Función `draw_sidebar()`

Dibuja toda la barra lateral derecha con:
- Estado de conexión
- Controles disponibles
- Leyenda de símbolos
- Estadísticas generales
- Info detallada del planeta seleccionado

Es puro Pygame dibujando texto, nada complejo.

### Función `main()`

El corazón del programa. Es el loop principal que:
1. Inicializa todo (carga datos, crea planetas)
2. Entra en un bucle infinito que:
   - Procesa eventos (clicks, teclas)
   - Actualiza física si no está pausado
   - Dibuja todo en pantalla
   - Se repite 60 veces por segundo

Básicamente: lee input → calcula física → dibuja → repite.

## Datos técnicos interesantes

- **TIMESTEP**: Cada "tick" de la simulación representa 1 día (86,400 segundos). Puedes cambiarlo con las flechas.
- **AU (Unidad Astronómica)**: Es la distancia Tierra-Sol (≈150 millones de km). Se usa para medir distancias en el sistema solar.
- **G (Constante Gravitacional)**: 6.67428e-11. Es la constante de la ley de Newton que usamos para calcular fuerzas.
- **SCALE**: Factor de reducción para ajustar distancias reales a la pantalla.

## Sistema de colores

- **Verde**: Precisión alta, todo bien
- **Naranja**: Advertencia, hay desviación
- **Rojo**: Error grande
- **Cyan**: Elementos seleccionados o títulos
- **Amarillo**: El Sol y títulos importantes

## Problemas comunes

**"No module named 'pygame'"**: No instalaste pygame. Corre `pip install pygame`

**La ventana se ve rara**: Está diseñada para 1920x1080. Si tu pantalla es más pequeña, edita las variables `WIDTH` y `HEIGHT` al inicio del código.

**Los planetas se mueven muy rápido/lento**: Usa las flechas arriba/abajo para ajustar la velocidad de tiempo.

**No se ve nada**: El espacio es oscuro! Espera unos segundos, los planetas empezarán a moverse.

## Ideas para mejorar (si quieres modificarlo)

- Conectar a la API real de NASA Horizons
- Agregar más planetas (Urano, Neptuno)
- Agregar lunas
- Hacer zoom con la rueda del mouse
- Permitir arrastrar la vista
- Agregar efectos de sonido
- Grabar las órbitas y hacer replay

## Referencias

Las fórmulas físicas vienen de:
- https://fiftyexamples.readthedocs.io/en/latest/gravity.html
- Tutorial de simulación orbital: https://www.youtube.com/watch?v=WTLPmUHTPqo

Los datos planetarios son aproximaciones de las órbitas reales pero simplificadas.

---

**Nota**: Este es un proyecto educativo. Las órbitas están simplificadas (son circulares cuando en realidad son elípticas) y hay muchas aproximaciones. Pero es suficientemente preciso para entender cómo funciona la física orbital!
