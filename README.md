# TFG-Santiago

Repositorio donde se encuentran algunos scripts creados durante el desarrollo del TFG. Una breve descripción de cada uno de ellos sería:

- convert.py: El objetivo final de este programa es traducir los datos de fijaciones que se encuentran normalmente en un fichero .csv con un formato determinado (incluido en el dataset correspondiente), y obtener al final los mapas de saliencia o de fijaciones que se usarán más adelante. Se van construyendo los diferentes mapas de fijaciones de cada fotograma, y para obtener los mapas de saliencia se le aplica un filtrado gaussiano con un sigma configurable, pudiendo guardar los resultados como imágenes y/o como ficheros .mat para poder usarlos en programas de Matlab.
    
- heatmaps.py: Este programa trata de colorear un mapa de saliencia (en este caso serán los predichos por el modelo), utilizando un mapa de color configurable, y en este caso se ha utilizado el viridis. Esto se hace para que sea más sencillo identificar las zonas más significativas del mapa de saliencia.
    
- assembling.py: En este programa se juntan los fotogramas reales de un vídeo con sus respectivos mapas de saliencia coloreados. Así, se puede ver rápidamente si las zonas predichas son consistentes con lo que se ve en el vídeo.
    
- gen_videos.py: Este programa coge todos los fotogramas generados con el script assembling.py para un determinado vídeo, y genera con ellos un vídeo en formato .mp4. Para ello es importante especificar bien los FPS con los que se quiere reconstruir el vídeo, ya que si no coinciden con los FPS usados para generar los frames, el vídeo resultante no será correcto.
    
- copy_sound.py: Con este programa se junta el .mp4 generado con el script anterior y un archivo de audio que contiene el sonido de dicho vídeo.
    
- eval_single_video.m: Con este programa de Matlab se evalúa un vídeo, utilizando por una parte los mapas de saliencia generados por el modelo, y por otra parte tanto los mapas de saliencia como de fijaciones que representan el ground truth, los cuales se han generado con el programa convert.py. Finalmente, se obtienen los valores de CC y de KL de dicho vídeo.
    
- eval_multiple_videos.m: Este programa repite el proceso del anterior para un conjunto de vídeos, lo cual se puede utilizar para evaluar el desempeño de un modelo de predicciones para los datos de test.
