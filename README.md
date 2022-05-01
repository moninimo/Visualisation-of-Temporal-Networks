# Visualisation-of-Temporal-Networks
A web application to visualising temporal networks.

## Introduction
This web application contains four methods at the moment.
#### Node Link 1 :
A series node-link diagrams on a timeline with constant node positions, and edges change over times.

#### Node Link 2 :
A time-stamp decorated, aggregated graph. The labels of the edges denotes the contacts between the nodes.

#### Juxtaposed :
A node-centric time line, where a vertical line represents a contact between two connected individual at the time given by the x-axis.

#### Animation :
A mapping of timestamps assigned to a sequence of graphs to visualization time results in an animated representation.


## Usage
#### Renter the website
Please enter following on terminal.
```
python app.py
```
#### The upload csv must in follwing format
| Num(int) | node1(str) | node2(str) | start(int) | end(int) | 
| :---: | :---: | :---: | :---: | :---: |
| 0 | A | B | 1 | 2 | 
| 1 | B | C | 2 | 3 | 
| 2 | B | D | 3 | 4 | 
| 3 | C | E | 4 | 6 | 
| 4 | D | F | 5 | 6 | 

## File Structure
```
- app.py
- pages
   |-- Homepage.py
   |-- animation.py
   |-- juxtaposed.py
   |-- node_link1.py
   |-- node_link2.py
```
You can add a new page by adding a new file under pages folder.

After implmented the new page, on app.py: 
- Import the new page
- Create a new navigation item
- Add a new call back

