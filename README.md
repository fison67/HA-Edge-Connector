# HA-Edge-Connector

1. Required<br/>
 a. Smartthings Hub & Homeassistant must be in same network.<br/>
 b. Multicast function must be enabled on router.<br/>
 <br/><br/>
2. Install<br/>
 a. Copy st_edge_connector folder to /YOUR_HA_PATH/custom_components<br/>
 b. Add a ST Edge Connector on integrations <br/>
   HUB ADDR: ST HUB Address.<br/>
   HA ADDR: HA Address.<br/>
   HA PORT: Non used port for TCP<br/>
<br/><br/>
3. ADD<br/>
  a. Add a device on st_edge_connector.<br/>
  b. Add a device on smartthings app<br/>
<br/><br/>
4. Support devices.<br/>
  a. HA Switch<br/>
     Without attributes [power, energy]<br/>
     switch.samplename<br/>
  b. HA Plug<br/>
     With attributes [power, energy]<br/>
     switch.samplename<br/>
  c. HA Light<br/>
     With attributes supported_color_modes [color_temp]<br/>
     light.samplename<br/>
  d. HA White Light<br/>
     With attributes supported_color_modes [brigtness]<br/>
     light.samplename<br/>
  e. HA Cover<br/>
     cover.samplename<br/>
  f. HA Motion<br/>
     With attributes [occupancy, battery]<br/>
     binary_sensor.samplename<br/>
  g. HA Contact<br/>
     With attributes [contact, battery]<br/>
     binary_sensor.samplename<br/>
