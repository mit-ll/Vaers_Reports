# Vaers_Reports
**VAERS data mining reports**

**Authors:** Darrell O. Ricke, Ph.D. (Darrell.Ricke@ll.mit.edu)

**RAMS request ID 1026632**

**Overview:** This program generates multiple reports on selected adverse events reported to the Vaccine Adverse
Event Reporting System (VAERS) database.

**Citation:** Ricke, D.O. & Smith, N.  Etiology Model of Kawasaki Disease and Multisystem Inflammatory Syndromes

**Disclaimer:**

DISTRIBUTION STATEMENT A. Approved for public release. Distribution is unlimited.

This material is based upon work supported by the Department of the Air Force 
under Air Force Contract No. FA8702-15-D-0001. Any opinions, findings, conclusions 
or recommendations expressed in this material are those of the authors) and do 
not necessarily reflect the views of the Department of the Air Force.

© 2023 Massachusetts Institute of Technology.

The software/firmware is provided to you on an As-Is basis

Delivered to the U.S. Government with Unlimited Rights, as defined in DFARS
Part 252.227-7013 or 7014 (Feb 2014). Notwithstanding any copyright notice,
U.S. Government rights in this work are defined by DFARS 252.227-7013 or
DFARS 252.227-7014 as detailed above. Use of this work other than as specifically
authorized by the U.S. Government may violate any copyrights that exist in this work.

This program is free software: you can redistribute it and/or modify
it under the terms of the GNU General Public License as published by
the Free Software Foundation, either version 2 of the License, or
(at your option) any later version.

This program is distributed in the hope that it will be useful,
but WITHOUT ANY WARRANTY; without even the implied warranty of
MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
GNU General Public License for more details.

## Overview

**Example input:** kawasaki.txt

    Kawasaki's disease

**To run:**

    python vaers_report.py <adverse events file> > <results file>

    python vaers_report.py kawasaki.txt > Kawasaki.tsv

**Output reports:**

  - Adverse event reports by vaccine code, number of shots, and normalized frequency per 100,000 VAERS reports
  - Adverse event reports by vaccine name, number of shots, and normalized frequency per 100,000 VAERS reports
  - Adverse event reprots by age and vaccine code, -1 designates that no age was entered
  - Adverse event reprots by age and vaccine code, -1 designates that no age was entered: (adverse events|total reports|normalized frequency per 100,000 reports)
  - Adverse event reprots by day of onset and vaccine code, -1 designates that no day of onset was entered
  - Adverse event reports by number of concurrent shots and vaccine code
  - Adverse event reports by number of concurrent shots and vaccine code: (adverse events by # of shots|total reports|normalized frequency per 100,000 reports)
  - Adverse event reports by number of concurrent shots and vaccine code for children age 0-5: (adverse events by # of shots|total reports|normalized frequency per 100,000 reports)
  - Details report on VAERS reports


