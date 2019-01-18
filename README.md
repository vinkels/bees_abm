# jiteyareta
Agent Based Modelling

## Bijen:
- food coordinate when found
- food quality (utility value)
- accuracy of giving food direction
- energy/fatigue of bee
- bee maximum travel distance
- range vision
- bee type

## Food:
- utility value
- location
- regeneration rate
- type (optional)

## Area:
- height
- width
- txt map of all elements
- number of hives

## Obstacles:
- type -> can bees fly over (extra distance)
- size
- coordinates

<div>Icons made by <a href="https://www.freepik.com/" title="Freepik">Freepik</a> from <a href="https://www.flaticon.com/" 			    title="Flaticon">www.flaticon.com</a> is licensed by <a href="http://creativecommons.org/licenses/by/3.0/" 			    title="Creative Commons BY 3.0" target="_blank">CC 3.0 BY</a></div>

## Food strategy and Hive balance:
 - Wanneer er meer food is dan gaat de reproductie rate omhoog en eten bijen meer
 - Als er weinig food is dan gaat het omlaag
 - Als de hoeveelheid food in de hive heel erg laag is, geen reproductie
 - Afhankelijk van de reproduction rate worden meer resters geboren
 - In Resters Class:
    > Als bijen in de hive aankomen worden het resters
    > Als bepaalde energy level hebben random nu tussen (5, 40) en er zijn food location bekend in de hive , dan worden de resters foragers
    >Als er geen locatie bekend is of ze hebben niet genoeg energie dan blijven ze resters en eten in de hive en sparen ze energie
    > Als er niet genoeg eten in de hive dan kost het de resters bij energie
 


