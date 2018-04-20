# HBondMachineLearning

Given two protein residue backbones floating in space,
I want to be able to predict which pairs of amino acids
would be able to form hydrogen bonds.
This could save us time and memory in protocols such as HBNet by
eliminating amino acids from the packer task at the very beginning of the protocol
if they are not predicted to be able to form hydrogen bonds.

## Results

|   |          D          |          E          |          H          |          K          |          N          |          Q          |          R          |          S          |          T          |          W          |          Y          |   |
| - |          -          |          -          |          -          |          -          |          -          |          -          |          -          |          -          |          -          |          -          |          -          | - |
| D |                    ?|                     |                     |                     |                     |                     |                     |                     |                     |                     |                     | D |
| E |                    ?|                    ?|                     |                     |                     |                     |                     |                     |                     |                     |                     | E |
| H |                    .|                    .|                    .|                     |                     |                     |                     |                     |                     |                     |                     | H |
| K |                    .|                    .|                    .|                    ?|                     |                     |                     |                     |                     |                     |                     | K |
| N |                    .|                    .|                    .|                    .|                    .|                     |                     |                     |                     |                     |                     | N |
| Q |                    .|                    .|                    .|                    .|                    .|                    .|                     |                     |                     |                     |                     | Q |
| R |                    .|[x](E_R_hbond/LOG.md)|                    .|                    ?|                    .|                    .|                    ?|                     |                     |                     |                     | R |
| S |                    .|                    .|                    .|                    .|                    .|                    .|                    .|[x](S_S_hbond/LOG.md)|                     |                     |                     | S |
| T |                    .|                    .|                    .|                    .|                    .|                    .|                    .|                    .|                    .|                     |                     | T |
| W |                    .|                    .|                    .|                    ?|                    .|                    .|                    ?|                    .|                    .|                    ?|                     | W |
| Y |                    .|                    .|                    .|                    .|                    .|                    .|                    .|                    .|                    .|                    .|                    .| Y |
|   |          D          |          E          |          H          |          K          |          N          |          Q          |          R          |          S          |          T          |          W          |          Y          |   |

Legend:

| Symbol | Meaning |
| ------ | ------- |
| x      | Job is done. The 'x' should contain a link to the log file for that job |
| .      | Job has not been done yet |
| ?      | Job has been skipped due to the inability for these residues to form hydrogen bonds |
| (blank)| This cell is redundant, check the bottom left corner of the chart for it's twin |