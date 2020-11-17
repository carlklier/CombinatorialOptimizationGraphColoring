# Project-B2-GraphColoring

### Authors
* Carl Klier

* Nachiket Patel

## Outline

## D-Wave
### Prerequisites
### Usage


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
