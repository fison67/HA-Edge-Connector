# HA-Edge-Connector

1. Required
 a. Smartthings Hub & Homeassistant must be in same network.
 b. Multicast function must be enabled on router.
 
2. Install
 a. Copy st_edge_connector folder to /YOUR_HA_PATH/custom_components
 b. Add a ST Edge Connector on integrations 
   HUB ADDR: ST HUB Address.
   HA ADDR: HA Address.
   HA PORT: Non used port for TCP
   
3. ADD
  a. Add a device on st_edge_connector.
  b. Add a device on smartthings app
  
4. Support devices.
  a. HA Switch
     Without attributes [power, energy]
     switch.samplename
  b. HA Plug
     With attributes [power, energy]
     switch.samplename
  c. HA Light
     With attributes supported_color_modes [color_temp]
     light.samplename
  d. HA White Light
     With attributes supported_color_modes [brigtness]
     light.samplename
  e. HA Cover
     cover.samplename
  f. HA Motion
     With attributes [occupancy, battery]
     binary_sensor.samplename
  g. HA Contact
     With attributes [contact, battery]
     binary_sensor.samplename
