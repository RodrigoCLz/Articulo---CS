# Análisis complementario del experimento (pendiente)

**Para:** compañero(a) responsable del análisis y del artículo.
**Estado:** pendiente. Ningún cálculo de esta lista se ha hecho todavía.
**Fecha de redacción:** 2026-11-23.

## Reglas que no se negocian

1. **No se llama a ningún modelo.** Todo sale de `resultados/experimento/episodios.csv` y `llamadas.jsonl`.
2. **No se cambia el análisis confirmatorio.** H1, H2 y H3 y sus cifras (`analisis/analizar_experimento.py`, `analisis/h3_mutantes.py`) quedan como están. Los cálculos nuevos van en un script aparte.
3. **Todo lo nuevo se etiqueta como exploratorio o complementario**, tanto en el código como en el texto del artículo.
4. **La unidad de análisis sigue siendo la tarea** (D-03). Las repeticiones y los modelos no se tratan como observaciones independientes.
5. **Los cuatro truncados cuentan como fallos** en el análisis principal (D-36). Solo se usan en la sensibilidad del punto 4.

## Contexto de los datos

- 1 200 episodios: 50 tareas × 3 condiciones (A, B, C) × 4 repeticiones × 2 modelos.
- Tamaños de tarea: 20 S, 20 M y 10 L.
- Columnas útiles de `episodios.csv`: `tarea`, `categoria`, `tamano`, `condicion`, `modelo`, `repeticion`, `iteraciones`, `resuelta_bucle`, `resuelta_heldout`, `truncado`, `tokens_total`.
- Hallazgo que hay que recordar: **B nunca reintentó** (400 de 400 episodios con una sola iteración). `resuelta_bucle` en B es solo la comprobación de ejecución.

## Tarea 1. Concordancia entre el bucle de C y la suite reservada

**Pregunta:** ¿qué tan bien coinciden las comprobaciones del bucle de C con la evaluación reservada?

**Qué calcular**
- Para los 400 episodios de C, una tabla 2×2 con `resuelta_bucle` × `resuelta_heldout`.
- Medidas descriptivas: porcentaje de acuerdo, y la proporción de aprobados del bucle que fallan en la reservada (falsos positivos del bucle) y al revés (falsos negativos).
- Desglose por modelo.
- Opcional: kappa de Cohen, reportada como descriptiva.

**Entradas:** `episodios.csv`, filas con `condicion == "C"`.

**Salida:** tabla en `resultados/experimento/complementario.md`, sección "Concordancia".

**Advertencia para el texto:** solo describe cómo coincidieron dos comprobaciones en estos episodios. No mide la calidad de C en general.

## Tarea 2. Resultados por tamaño de tarea (S, M, L)

**Pregunta:** ¿cambia la tasa y la diferencia C − B según el tamaño de la tarea?

**Qué calcular**
- Por tamaño y condición: tasa de resolución (media por tarea, promediando repeticiones y modelos).
- Diferencia C − B por tamaño, con IC95 % bootstrap sobre tareas (10 000 remuestreos, semilla fija).
- Tabla con n de tareas por grupo: 20 S, 20 M, 10 L.

**Advertencia:** con 10 tareas grandes, el IC de L será amplio. Reportar sin interpretar causalmente. No presentar como conclusión.

**Salida:** sección "Por tamaño" en `complementario.md`, y una figura opcional `paper/figuras/tamano.pdf`.

## Tarea 3. Variabilidad por tarea

**Pregunta:** ¿la mejora de C se reparte entre las tareas o se concentra en unas pocas?

**Qué calcular**
- Para cada una de las 50 tareas: tasa de C, tasa de B, tasa de A y diferencia C − B. Cada tasa promedia 8 episodios (4 repeticiones × 2 modelos).
- Conteo: cuántas tareas favorecen a C, cuántas empatan y cuántas favorecen a B.
- Gráfica de intervalos o puntos por tarea, ordenada por diferencia, con la línea de 0.

**Advertencia:** con 8 episodios por tarea, cada diferencia tiene granularidad de 1/8. El conteo es descriptivo; no reemplaza el contraste de H1.

**Salida:** tabla de conteos en `complementario.md`, y figura `paper/figuras/por_tarea.pdf`.

## Tarea 4. Sensibilidad a los cuatro truncados

**Pregunta:** ¿cambian las conclusiones si los cuatro truncados de C se tratan de otra forma?

**Qué calcular**
- Límite favorable a C: recalcular la diferencia C − B suponiendo que los cuatro episodios truncados hubieran resuelto la tarea.
- Límite desfavorable a C: los cuatro cuentan como fallos (es el análisis principal, ya calculado).
- Opcional, menos recomendado: excluir los cuatro episodios. Hay que decir que favorece artificialmente a C porque elimina solo episodios de esa condición.

**Advertencia:** la sensibilidad se etiqueta como **post hoc**. El resultado preregistrado sigue siendo el principal.

**Salida:** sección "Sensibilidad a truncados" en `complementario.md`.

## Implementación sugerida

1. Crear `analisis/complementario.py`, que lea solo los CSV y escriba `resultados/experimento/complementario.md`.
2. Usar la misma semilla de bootstrap que las métricas complementarias ya existentes (`SEED + 1` en `analizar_experimento.py`), o una semilla nueva registrada en `DECISIONES.md`.
3. Añadir pruebas en `tests/` para la tabla 2×2 y el conteo por tarea, con datos sintéticos.
4. Regenerar figuras con `analisis/figuras.py` si se agregan figuras nuevas.
5. Actualizar `paper/articulo.tex` solo con cifras que salgan de `complementario.md`, y marcar cada una como complementaria.
6. Registrar la decisión en `DECISIONES.md` antes de publicar el artículo.

## Criterios de terminado

- [ ] `complementario.py` corre sin llamadas a modelos y produce `complementario.md`.
- [ ] Pruebas nuevas pasan y las 63 existentes siguen pasando.
- [ ] El análisis confirmatorio no cambió (comparar `analisis.md` antes y después).
- [ ] Cada resultado nuevo aparece etiquetado como exploratorio, complementario o post hoc.
- [ ] El artículo no usa ninguna cifra que no esté en `complementario.md` o en los análisis confirmatorios.
- [ ] Decisión registrada en `DECISIONES.md`.

## Qué no entra en este trabajo

- Ruido, propiedades metamórficas, comprobaciones estáticas y aserciones dinámicas de C, tiempos por llamada: no se midieron ni se implementaron. Requieren un estudio nuevo con su propio preregistro.
- Desglose de H3 por familia de mutantes: es posible, pero requiere volver a correr el análisis local de mutantes. Se decide aparte.
