# Baratieri's War Council Console (የባራቲየሪ ድንብርብር)

**Category:** Web Exploitation  
**Difficulty:** Hard (1000 points)  
**Historical Setting:** Italian Forward Encampment at Sauria — Night of 29 February 1896  

## Narrative Background
On the eve of the historic clash, Lieutenant General Oreste Baratieri convened his council of war at the forward encampment of Sauria alongside brigade commanders Albertone, Arimondi, Dabormida, and Ellena. Facing dwindling rations and pressure from Prime Minister Crispi in Rome, Baratieri finalized the fateful night march order toward the Adwa basin.

Field transmissions and brigade dispatches were drafted and distributed via the headquarters' field telegraph console. The terminal features an automated security filter designed to purge subversive dispatches before rendering the official orders.

## Artifacts Provided
- `app.py`: Source code of the field telegraph console web interface and security filter.
- `console_notice.txt`: Field headquarters notice from the Sauria transmission bureau.

## Objective
Analyze the console application, identify weaknesses in the dispatch template processing pipeline, and bypass the military inspection filter to execute an administrative readout and recover the confidential command flag.

## Flag Format
`AdwaCTF{...}`
