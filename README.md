# Myo-scope
Myo-scope is a tool to visialize the emg and angle data collected or caculated by multiple Myo armbands.It is base on Niklas' Python bindings for the Myo SDK: [myo-python](https://github.com/NiklasRosenstein/myo-python) and enthought company's traits-capable windowing framework:[traitUI](https://github.com/enthought/traitsui).<br>
## example list
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
	* [enable](https://github.com/enthought/enable)
* [myo-python](https://github.com/NiklasRosenstein/myo-python)
