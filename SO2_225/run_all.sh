
sander -O -i md_inputs/0_min.in -o md_outputs/0_min.out -p md_inputs/water_solvated.prmtop -c md_inputs/water_solvated.inpcrd -r checkpoints/0_min.rst
sander -O -i md_inputs/1_heating.in -o md_outputs/1_heating.out -p md_inputs/water_solvated.prmtop -c checkpoints/0_min.rst -r checkpoints/1_heating.rst -x ptraj/1_heating.mdcrd 
sander -O -i md_inputs/2_eq.in -o md_outputs/2_eq.out -p md_inputs/water_solvated.prmtop -c checkpoints/1_heating.rst -r checkpoints/2_eq.rst -x ptraj/2_eq.mdcrd 
sander -O -i md_inputs/3_eq-so2.in -o md_outputs/3_eq-so2.out -p md_inputs/water_solvated.prmtop -c checkpoints/2_eq.rst -r checkpoints/3_eq.rst -x ptraj/3_eq.mdcrd
sander -O -i md_inputs/4_production.in -o md_outputs/4_production.out -p md_inputs/water_solvated.prmtop -c checkpoints/3_eq.rst -r checkpoints/4_production.rst -x ptraj/production.mdcrd

