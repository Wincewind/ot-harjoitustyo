

## Tehtävä 4

```mermaid

sequenceDiagram
    main->>laitehallinto: HKLLaitehallinto()
    main->>rautatietori: Lataajalaite()
    main->>ratikka6: Lataajalaite()
    main->>bussi244: Lataajalaite()
    main->>laitehallinto: lisaa_lataaja(rautatietori)
    main->>laitehallinto: lisaa_lataaja(ratikka6)
    main->>laitehallinto: lisaa_lataaja(bussi244)
    main->>lippu_luukku: Kioski()
    main->>lippu_luukku: osta_matkakortti("Kalle")
    activate lippu_luukku
    lippu_luukku->>kallen_kortti: Matkakortti("Kalle")
    lippu_luukku-->>main: 
    deactivate lippu_luukku
    main->>rautatietori: lataa_arvoa(kallen_kortti, 3)
    activate rautatietori
    rautatietori->>kallen_kortti: kasvata_arvoa(3)
    rautatietori-->>main: 
    deactivate rautatietori
    main->>ratikka6: osta_lippu(kallen_kortti, 0)
    activate ratikka6
    ratikka6->>kallen_kortti: vahenna_arvoa(1.5)
    ratikka6-->>main: True
    deactivate ratikka6
    main->>bussi244: osta_lippu(kallen_kortti, 2)
    activate bussi244
    bussi244-->>main: False
    deactivate bussi244
    
```
