# HBondMachineLearning
Trying to use Keras to predict the HBNet interaction energies between two residues given only their relative backbone coordinates.

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