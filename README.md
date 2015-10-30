# FlowRunner
Repository for preparing and running benchmark tests in project [Flow123d](https://github.com/flow123d/flow123d).

## Structre
All py files are in flowrunner package to avoid conflicts (since Python here will run binary which will again run Python there can be conflict in path). All scripts in this repo beginning with ```script_``` can be executed within source dir (```sys.path``` is altered).

### 3rd party libraries
By default paths ```./libs``` and ```./lib``` are added to sys.path to support 3rd party libraries.
