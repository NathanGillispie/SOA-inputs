cd outputs
../process_mdout.perl ../2_eq-app.out && gnuplot < ../plotNorm
../process_mdout.perl ../2_eq-therm-app.out && gnuplot < ../plotTherm
../process_mdout.perl ../2_eq-dipole.out && gnuplot < ../plotDip
