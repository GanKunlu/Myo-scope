# -*- coding: utf-8 -*-
from traits.api import *
from traitsui.api import *
from chaco.api import Plot, AbstractPlotData, ArrayPlotData, VPlotContainer, Legend
from enable.api import Component, ComponentEditor 
from pyface.timer.api import Timer
import time
import numpy as np
from myo import init, Hub, Feed, StreamEmg
import Myos_angle
from collections import deque 
	
class AnimationHandler(Handler):
	def init(self, info):
		super(AnimationHandler,self).init(info)
		info.object.timer = Timer(80,info.object.on_timer)
	
	def closed(self, info, is_ok):
		super(AnimationHandler,self).closed(info,is_ok)
		info.object.timer.Stop()		

class MYOGrapher(HasTraits):
	
	sEMG_length = Range(100,600,150)
	Angle_length = Range(80,300,120)
	sEMG_names = List(Str)
	Angle_names = List(Str)
	Which_Myo_sEMG = Enum(['myo1','myo2'])
	select_emg_names = List(Str)
	select_angle_names = List(Str)
	plot_EMG = Instance(Plot)
	plot_Angle = Instance(Plot)
	data_EMG = Instance(ArrayPlotData)
	data_Angle = Instance(ArrayPlotData)
	stream_emg = List(deque)
	stream_Angle = List(deque)
	traits_view=View(	
				HSplit(# HSplit分为左右两个区域，中间有可调节宽度比例的调节手柄
					   # 左边为一个组		
						VSplit(
							VGroup(
								Item("Which_Myo_sEMG", label=u"肌电信号源 "),
								Item("sEMG_length", label=u"肌电横轴范围 " ),
								Item("select_emg_names",style="custom", label=u"肌电通道选择 ",
								editor=CheckListEditor(name="object.sEMG_names", 
									cols=2, format_str=u"%s")),
								show_border = True, # 显示组的边框
								scrollable = True,  # 组中的控件过多时，采用滚动条
								),
							VGroup(	
								Item("Angle_length", label=u"角度横轴范围 "),
								Item("select_angle_names",style="custom", label=u"选择手环 ",
								editor=CheckListEditor(name="object.Angle_names", 
									cols=2, format_str=u"%s")),
								show_border = True, # 显示组的边框
								scrollable = True,  # 组中的控件过多时，采用滚动条
								)
							),
						VGroup(
							Item("plot_EMG", editor = ComponentEditor(),show_label=False,width=700, height=100),
							Item("plot_Angle", editor = ComponentEditor(),show_label=False,width=700, height=100),
							show_border = True, # 显示组的边框
							)
						),
					resizable = True,
					height = 500,
					width = 1000,
					title = u"MYO数据信号示波器",
					handler = AnimationHandler()
					)
		
	def __init__(self,**traits):
		super(MYOGrapher, self).__init__(**traits)
		
		data_EMG = ArrayPlotData(x=[0],sEMG1=[0],sEMG2=[0],sEMG3=[0],
			sEMG4=[0],sEMG5=[0],sEMG6=[0],sEMG7=[0],sEMG8=[0])
		data_Angle = ArrayPlotData(x=[0],myo1=[0],myo2=[0])
		
		plot_Angle = Plot(data_Angle)
		plot_EMG = Plot(data_EMG)
		
		plot_EMG.plot(("x","sEMG1"),type="line")
		plot_EMG.title = "sEMG"
		plot_EMG.value_scale = 'linear'
		
		plot_Angle.plot(("x","myo1"),type="line")
		plot_Angle.title = "Angle"
		plot_Angle.value_scale = 'linear'
		
		self.plot_EMG = plot_EMG
		self.data_EMG = data_EMG
		
		self.plot_Angle = plot_Angle
		self.data_Angle = data_Angle
		
		self.sEMG_names = ['sEMG1','sEMG2','sEMG3',
			'sEMG4','sEMG5','sEMG6','sEMG7','sEMG8']
		self.Angle_names = ['myo1','myo2']
		
		_stream_emg = []
		_stream_angle = []
		for chanel in range(8):
			_stream_emg.append(deque(np.zeros(self.sEMG_length)))
		self.stream_emg = _stream_emg
		for _myos_in in range(2):
			_stream_angle.append(deque(np.zeros(self.Angle_length)))
		self.stream_Angle =_stream_angle
	def _select_emg_names_changed(self):
		for chanel in range(8):
			self.stream_emg[chanel] = deque(np.zeros(self.sEMG_length))
		self.plot_EMG = Plot(self.data_EMG)
		self.plot_EMG.auto_colors = ['green', 'lightgreen','blue', 
			'lightblue', 'red', 'pink', 'darkgray', 'silver']
		for pic in self.select_emg_names:
			self.plot_EMG.plot(('x',)+(pic,),name = pic,color = 'auto')
		self.plot_EMG.title='Multiple sEMG'
		legend = Legend(padding=10,align="ur")
		legend.plots = self.plot_EMG.plots
		self.plot_EMG.overlays.append(legend) 		
	
	def _select_angle_names_changed(self):
		for _myos_in in range(2):
			self.stream_Angle[_myos_in] = deque(np.zeros(self.Angle_length))
		self.plot_Angle = Plot(self.data_Angle)
		self.plot_Angle.auto_colors = ['blue','red']
		for _pic in self.select_angle_names:
			self.plot_Angle.plot(('x',)+(_pic,),name = _pic,color = 'auto')
		self.plot_Angle.title='Multiple Angle'
		_legend = Legend(padding=10,align="ur")
		_legend.plots = self.plot_Angle.plots
		self.plot_Angle.overlays.append(_legend)
			
	@on_trait_change("sEMG_length, Which_Myo_sEMG")
	def init_semgdata(self):
		for chanel in range(8):
			self.stream_emg[chanel] = deque(np.zeros(self.sEMG_length))
	
	@on_trait_change("Angle_length")
	def init_angledata(self):
		for in_myo in range(2):
			self.stream_Angle[in_myo] = deque(np.zeros(self.Angle_length))
	
	def on_timer(self):
		global myo_device
		myos = 0
		if self.Which_Myo_sEMG == 'myo2':
			myos = 1
		if len(self.select_emg_names)!=0:
			for name in self.select_emg_names:
				index = self.sEMG_names.index(name)
				self.stream_emg[index].appendleft(myo_device[myos].emg[index])
				self.stream_emg[index].pop()
				self.data_EMG[name] = np.array(self.stream_emg[index])
		self.data_EMG['x'] = range(self.sEMG_length)
		
		if len(self.select_angle_names)!=0:
			for _name1 in self.select_angle_names:
				_index1 = self.Angle_names.index(_name1)
				self.stream_Angle[_index1].appendleft(Myos_angle.angle_init(myo_device,[0,0],[_index1])[0])
				self.stream_Angle[_index1].pop()
				self.data_Angle[_name1] = np.array(self.stream_Angle[_index1])
		self.data_Angle['x'] = range(self.Angle_length)		
				
if __name__ == "__main__":
	init()
	feed = Feed()
	hub = Hub()
	times = 0
	hub.run(1000, feed)	
	try:
		myo_device = feed.get_devices()
		print(myo_device)
		time.sleep(1)
		myo_device[0].set_stream_emg(StreamEmg.enabled)
		myo_device[1].set_stream_emg(StreamEmg.enabled)
		MYO_Grapher = MYOGrapher()
		MYO_Grapher.configure_traits() 
	finally:
		hub.shutdown()
		