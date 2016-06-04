# Myo-scope
Myo-scope is a tool to visialize the emg and angle data collected or caculated by multiple Myo armbands.It is base on Niklas' Python bindings for the Myo SDK: [myo-python](https://github.com/NiklasRosenstein/myo-python) and enthought company's traits-capable windowing framework: [traitUI](https://github.com/enthought/traitsui).<br>
The interactive GUI is build with traitsUI. The dynamic figure of the data in our GUI is plot by Chaco which is a Python package for building interactive and custom 2-D plots and visualizations. Using this GUI program you can choose which Myo will be used and add any channels to the GUI in the window of EMG part. In the angle window, you can choose to plot the angle data calculated from any Myo.
## Example list
get_Multiple_Angle.py: Calculate the angle between the z-axis direction using the data of acceloration and gyroscope.<br>
Myo_scope.py: Create a GUI and visialize the emg and angle in a ranslational dynamic map.<br>
Myo_scope_edit.py: Create a GUI and visialize the emg and angle in a refreshing dynamic map.<br>
## Prerequisites
If you want to run this examples, you must also install:<br>
* [python2.7](https://www.python.org/)
* [traitsUI](https://github.com/enthought/traitsui)
	* [wxPython](http://www.wxpython.org/)
	* [traits](https://github.com/enthought/traits)
	* [pyface](https://github.com/enthought/pyface)
* [chaco](https://github.com/enthought/chaco)
	* distribute
	* numpy
	* [enable](https://github.com/enthought/enable)
* [myo-python](https://github.com/NiklasRosenstein/myo-python)
