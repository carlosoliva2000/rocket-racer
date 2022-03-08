from ray import tune
from rocket_racer import Juego

tune.run(run_or_experiment="SAC",
         checkpoint_freq=100,
         checkpoint_at_end=True,
         local_dir=r'./resultados',
         config={
             "env": Juego,
             "render_env": True,
             "env_config": {
                 "render": True
             }
         })
