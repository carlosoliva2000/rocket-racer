from ray import tune
from rocket_racer import Juego

tune.run(run_or_experiment="SAC",
         checkpoint_freq=100,
         checkpoint_at_end=True,
         local_dir=r'./resultados',
         config={
             "env": Juego,
             "render_env": True,
             "num_workers": 4
         }
         # ,
         # stop={
         #     "timestep_total": 5_000_000
         # }
         )
