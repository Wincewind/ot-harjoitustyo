## Tehtävä 3

```mermaid

sequenceDiagram
    main->>masiina: Machine()
    masiina->>tank: FuelTank()
    masiina->>tank: fill(40)
    masiina->>engine: Engine(tank)
    main->>masiina: drive()
    activate masiina
    masiina->>engine: start()
    activate engine
    engine->>tank: consume(5)
    deactivate engine
    masiina->>engine: is_running()
    activate engine
    engine->>tank: fuel_contents
    tank-->>engine: 35
    engine->>engine: 35 > 0
    engine-->>masiina: True
    deactivate engine
    masiina->>engine: use_energy()
    activate engine
    engine->>tank: consume(10)
    deactivate engine
    masiina-->>main: 
    deactivate masiina
    
```
