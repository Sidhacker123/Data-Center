
#!/bin/bash

cd plot

if [ -f cwnd-graph.png ]; then
	rm cwnd-graph.png
fi
if [ -f fct-graph.png ]; then
	rm fct-graph.png
fi

cd ..

echo python plot/parse-cwnd.py logs/h40-cwnd.txt logs/h20-cwnd.txt 
python plot/parse-cwnd.py logs/h40-cwnd.txt logs/h20-cwnd.txt 

echo python plot/plot-cwnd.py plot/h40-cwnd.dat plot/h20-cwnd.dat 
python plot/plot-cwnd.py plot/h40-cwnd.dat plot/h20-cwnd.dat

echo python plot/parse-fct.py
python plot/parse-fct.py

echo python plot/plot-fct.py
python plot/plot-fct.py
