# HA-Edge-Connector

<h3>Homeassistant to Smartthings</h3>
<br/><br/>

## Donation
If this project helps you, you can give me a cup of coffee<br/>
[![Donate](https://img.shields.io/badge/Donate-PayPal-green.svg)](https://paypal.me/fison67)
<br/><br/>

## Setup
<b>1. Required</b><br/>
&nbsp;&nbsp;a. Smartthings Hub & Homeassistant must be in same network.<br/>
&nbsp;&nbsp;b. Multicast function must be enabled on router.<br/>
&nbsp;&nbsp;c. This connector use an udp 30000 port.<br/>
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
&nbsp;&nbsp;&nbsp;&nbsp;h. HA Presence<br/>
&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;device_tracker.samplename<br/>

<br/><br/>
<b>5. Sample Images.</b><br/>
<img src="./imgs/edge_cordinator.png" width="500px"><br/>
<img src="./imgs/intergration.jpg" width="500px"><br/>
<img src="./imgs/device.png" width="500px"><br/>
<img src="./imgs/list.png" width="500px"><br/>
<br/><b>Pairing</b><br/>
<img src="./imgs/pairing.png" width="500px"><br/>
<br/><b>Plug</b><br/>
<img src="./imgs/plug.png" width="500px"><br/>
<br/><b>Light White</b><br/>
<img src="./imgs/light-white.png" width="500px"><br/>
<br/><b>Cover</b><br/>
<img src="./imgs/cover.png" width="500px"><br/>
<br/><b>Contact</b><br/>
<img src="./imgs/contact.png" width="500px"><br/>
<br/><b>Motion</b><br/>
<img src="./imgs/motion.png" width="500px"><br/>
