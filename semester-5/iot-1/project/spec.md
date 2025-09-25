# ChaosCam + AtmosNoise IoT Randomness Game
IoT1 University Project – Specification

## Project Overview
The goal of this project is to design and implement a distributed random number generator (RNG) system using three Raspberry Pis and real-world sensors. The entropy will be harvested from different environmental sources:

1. **Pi A (AtmosNoise Node):** Radio frequency noise (via SDR/AM radio).  
2. **Pi B (ChaosCam Node):** Image noise and motion entropy from a Raspberry Pi Camera.  
3. **Pi C (Aggregator & Game Node):** Collects entropy, performs randomness conditioning, and uses it to power a simple **luck-based game** (e.g., dice roll, wheel of fortune, or hot potato game).

This project demonstrates:
- Use of **IoT sensors** for non-traditional applications (randomness instead of measurement).
- **Networking between Pis** via MQTT broker.
- **Entropy quality comparisons** across multiple chaotic sources.
- Delivery of a **fun, interactive demo** backed by rigorous randomness principles.

## Goals
- Collect entropy from at least **two distinct environmental sources** (radio signals, camera sensor noise).
- Distribute the system across **three Raspberry Pis** interconnected by MQTT.
- Whiten and combine entropy sources into a single RNG stream using SHA-256 and DRBG.
- Provide a **web-based UI** to demonstrate randomness in an interactive game.
- Document and **evaluate entropy quality** with basic statistical tests.

## System Architecture

```{mermaid}
architecture-beta
    group iot_network(cloud)[IoT_Network]

    %% Pi A: AtmosNoise
    group pi_a_group(server)[PiA_AtmosNoise] in iot_network
    service sdr(disk)[SDR_AM_Radio] in pi_a_group
    service entropy_a(database)[EntropyExtractorA] in pi_a_group
    service pub_a(database)[MQTT_PublisherA] in pi_a_group

    %% Pi B: ChaosCam
    group pi_b_group(server)[PiB_ChaosCam] in iot_network
    service camera(disk)[PiCamera] in pi_b_group
    service entropy_b(database)[EntropyExtractorB] in pi_b_group
    service pub_b(database)[MQTT_PublisherB] in pi_b_group

    %% Pi C: Aggregator + Game
    group pi_c_group(server)[PiC_Aggregator_Game] in iot_network
    service broker(cloud)[MQTT_Broker] in pi_c_group
    service combiner(database)[EntropyCombiner] in pi_c_group
    service drbg(database)[DRBG] in pi_c_group
    service game(internet)[WebGameUI] in pi_c_group
    service stats(internet)[StatsDashboard] in pi_c_group

    %% Pi A flow
    sdr:R -- L:entropy_a
    entropy_a:R -- L:pub_a
    pub_a:R -- L:broker

    %% Pi B flow
    camera:R -- L:entropy_b
    entropy_b:R -- L:pub_b
    pub_b:R -- L:broker

    %% Pi C flow
    broker:R -- L:combiner
    combiner:R -- L:drbg
    drbg:R -- L:game
    combiner:B -- T:stats
```