# python-mqtt-sse
## System Diagram
```mermaid
graph TD
    M((man)) ---|count| AR
    AR["Arduino(distance sensor)"] -->|relay trigger| Relay
    Relay -->|"relay trigger"| RP
	RP[Raspberry Pi<br>MQTT-Pub/Sub] -->|pub: test/count|MQTT[[MQTT<br>ip: 10.100.100.220]]
    MQTT -->|sub: api/control|RP
    MQTT -->|sub: test/count|APP[Web Application<br>ip: 10.100.100.220]
    APP -->|pub: api/control|MQTT
    APP ---|redis| RD[(Redis Server<br>ip: 10.100.100.220)]
    RVPX[Reverse Proxy<br>ip: 202.44.73.30] -->|http| APP
    C([Client<br>ip: 10.10.x.x/24]) -->|http| RVPX

    subgraph IOT Devices
        AR
        Relay
        RP
    end

    subgraph Server Zone
        MQTT
        APP
        RVPX
        RD
    end
```
