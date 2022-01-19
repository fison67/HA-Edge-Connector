# HA-Edge-Connector

<b>1. Required</b><br/>
&nbsp;&nbsp;a. Smartthings Hub & Homeassistant must be in same network.<br/>
&nbsp;&nbsp;b. Multicast function must be enabled on router.<br/>
 <br/><br/>
<b>2. Install</b><br/>
&nbsp;&nbsp;a. Copy st_edge_connector folder to /YOUR_HA_PATH/custom_components<br/>
&nbsp;&nbsp;b. Add a ST Edge Connector on integrations <br/>
&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;HUB ADDR: ST HUB Address.<br/>
&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;HA ADDR: HA Address.<br/>
&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;HA PORT: Non used port for TCP<br/>
<br/><br/>
<b>3. ADD</b><br/>
&nbsp;&nbsp;a. Add a device on st_edge_connector.<br/>
&nbsp;&nbsp;b. Add a device on smartthings app<br/>
<br/><br/>
<b>4. Support devices.</b><br/>
&nbsp;&nbsp;&nbsp;&nbsp;a. HA Switch<br/>
&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;Without attributes [power, energy]<br/>
&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;switch.samplename<br/>
&nbsp;&nbsp;&nbsp;&nbsp;b. HA Plug<br/>
&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;With attributes [power, energy]<br/>
&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;switch.samplename<br/>
&nbsp;&nbsp;&nbsp;&nbsp;c. HA Light<br/>
&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;With attributes supported_color_modes [color_temp]<br/>
&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;light.samplename<br/>
&nbsp;&nbsp;&nbsp;&nbsp;d. HA White Light<br/>
&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;With attributes supported_color_modes [brigtness]<br/>
&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;light.samplename<br/>
&nbsp;&nbsp;&nbsp;&nbsp;e. HA Cover<br/>
&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;cover.samplename<br/>
&nbsp;&nbsp;&nbsp;&nbsp;f. HA Motion<br/>
&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;With attributes [occupancy, battery]<br/>
&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;binary_sensor.samplename<br/>
&nbsp;&nbsp;&nbsp;&nbsp;g. HA Contact<br/>
&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;With attributes [contact, battery]<br/>
&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;binary_sensor.samplename<br/>
