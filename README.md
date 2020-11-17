# Project-B2-GraphColoring

### Authors
* Carl Klier

* Nachiket Patel

## Outline

## D-Wave
### Prerequisites

* Running on the Dwave annealing system requires a D-Wave Leap account. You can make an account here: https://cloud.dwavesys.com/leap/signup/
* Once you sign into your Leap Account, you will see an API Token on your dashboard that you will need to install and setup the Dwave Ocean SDK below.
* You will also need to install the DWave Ocean SDK. For this, you will need python3 and pip3.
1.  pip3 install --user dwave-ocean-sdk
2.  dwave config create
3. Confirm configuration file path [...]: < PATH/FOR/FILE >
4. Profile (create new) [prod]: < NEW-PROFILE-NAME >
5. API endpoint URL [skip]: https://cloud.dwavesys.com/sapi
6. Authentication token [skip]: < YOUR-API-TOKEN >
7. Default client class (qpu or sw) [qpu]:
8. default solver: DW_2000Q_6 (see https://cloud.dwavesys.com/leap/)
9. dwave ping
10. Verify that you get a response from the 'dwave ping' command.

* other packages you will need include networkx, numpy, and matplotlib. These can be installed by running 'pytthon3 -m pip install <package>' with networkx, numpy, and matplotlib inserted for <package>. 

### Usage
The easiest way to run the majority of the Dwave annealing code is in a juypter notebook. Those files include: SimulatedKColoringCSP-3colors.ipynb, SimulatedKColoringCSP-4colors.ipynb, RealKColoringCSP-4colors.ipynb, RealKColoringCSP-4colors.ipynb. These files are also provided as python files. The python files will need to be run in an interactive window to view the graph outputs such as VSCode's interactive window with the Microsoft Python extension installed.

* 3-coloringCanada.PNG shows the 3 coloring we found for the Canada coloring problem
* 4-coloringCanada.PNG shows the 4 coloring provided by the Dwave documenation example
* DwaveTimeComplexity.PNG shows a graph of the qpu_access_time for finding 4 colorings for the 5 graphs seen in calculateDwaveTimeComplexity.py
* CanadaGraphColoringCSP.py is the code provided by the Dwave documenation as an example for solving the graph coloring problem
* ChromaticNumber.py finds the chromatic number by using real quantum hardware and plots the coloring for a graph
* RealChromaticNumber.ipynb finds the chromatic number by using real quantum hardward and plots its coloring for a graph
* RealKColoringCSP-3colors.ipynb notebook with code to solve the 3-coloring problem for our graph on real quantum hardware.
* RealKColoringCSP-4colors.ipynb notebook with code to solve the 4-coloring problem for our graph on real quantum hardware.
* SimulatedKColoringCSP-3colors.ipynb notebook with code to solve the 3-coloring problem for our graph on a quantum simulator.
* SimulatedKColoringCSP-4colors.ipynb notebook with code to solve the 4-coloring problem for our graph on a quantum simulator.
* RealKColoringCSP.py python file for solving the 3-coloring problem for our graph on real quantum hardware. 
* SimulatedKColoringCSP.py python file for solving the 3-coloring problem for our graph on a quantum simulator
* calculateDwaveTimeComplexity.py python code to plot a graph of the qpu_access_times for 5 increasingly larger graphs to understand how time increases as the graph size increase.
* simulatedChromaticNumber.py python file for finding the chromatic number by using a quantum simulator and plots the colorings for a graph

## IBM Qiskit
### Prerequisites
* Resuires python3 and pip3
* Must have Qiskit 0.23.1 python packages installed
  * Instruction can be obtained on qiskits site (https://qiskit.org/documentation/install.html)
* Jupyter notebooks are not required but the vast majority of code is in notebooks so it is recommended.

### Usage
* The 2-coloring (2-coloring.ipynb) code is sourced from (https://hal.archives-ouvertes.fr/hal-02891847/document) so for more information please read their paper
* All qiskit code is run on the paris backend, so you will require access
  to the paris backend or modify the code to use a different backend.
* Most notebooks have to be run from start to finish as asome variables are
  resued
* The results were obtained when the machine was configured with calibration specified in the file ibmq_paris_calibration_11-16-20.csv
* Running the code is simple, just execute all the cells from start to beginning, depending on your access to the qiskit backends the time taken to execute can very.

* 3-coloring-qiskit-real-OL#.ipyne - These notebooks contain the 3 coloring with different optimization level indicated by the #.
* 3-coloring-qiskit-real.ipyne contains results run on the paris backend
* 3-coloring-qiskit-sim.ipyne contains results run on the QASM simulator with pairs backend noise model
* 3-coloring-qiskit-real-runtime-test.ipyne results of testing the runtime of the qiskit machine as the size of the graph was increased.
* 4-coloring-qiskit-real.ipyne contains 4 coloring results run on the paris backend
* 4-coloring-qiskit-sim.ipyne contains 4 coloring results run on the QASM simulator with pairs backend noise model
