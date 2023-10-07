// 3D Game of Life
// Copyright (c) 2023 Ben Thomas


// Create an object for the game which includes generating the sides
var game = {

    // Some properties general to the whole game: 
    waitTime: 10,
    generation : 0,
    generationElement: null,
    mouseDown : false, 
    running : false,
    clear : false,
    sides : [],

    // Function that is run when the page loads and for cleaning up / resetting
    init : function(clear) {
        console.log("Initializing...");
        clear = (clear == undefined ? false : clear); 
        this.generation = 0;
        this.running = this.clear = false;
        this.generationElement = document.getElementById('generation');

        // Create objects for each side from the Side class below. 
        const world0 = new Side(0);
        const world1 = new Side(1);
        const world2 = new Side(2);
        const world3 = new Side(3);
        const world4 = new Side(4);
        const world5 = new Side(5);
        this.sides.push(world0)
        this.sides.push(world1)
        this.sides.push(world2)
        this.sides.push(world3)
        this.sides.push(world4)
        this.sides.push(world5)

        // Connect each Side object to the HTML side <div> and run functions to draw the world
        for (var s = 0; s < this.sides.length; s++) {
            this.sides[s].world = this.sides[s].newWorld = this.sides[s].cells = this.sides[s].age = null;
            this.sides[s].mouseDown = false;
            this.sides[s].table = document.getElementById('world'+this.sides[s].id);

            this.sides[s].initWorld();
            this.drawWorld(s);
        }
        
    },


    // Function to "draw" the side and register mouse clicks to each HTML <td>
    drawWorld : function(s) {
        console.log("Trying to draw world..."+s);
        var table = document.createElement('table');
        this.sides[s].cells = [];

        for (var i = 0; i < this.sides[s].edge; i++) {
            var line = document.createElement('tr');
            this.sides[s].cells[i] = [];
            for (var j = 0; j < this.sides[s].edge; j++) {
                var cell = document.createElement('td');
                cell.style.background = this.sides[s].colors.dead;

                this.addEvent(cell, 'mousedown', function(x, y) {
                    return function (event) {
                        game.cellMouseDownHandler(s, x, y, event);
                    }
                }(i, j));

                this.addEvent(cell, 'mouseup', function() {
                    return function () {
                        game.cellMouseUpHandler(s);
                    }
                }());

                line.appendChild(cell); 
                this.sides[s].cells[i][j] = cell; 
            }
            table.appendChild(line);
        }
        this.sides[s].table.appendChild(table); 
    },


    // Function to clear the world for the clear button
    clearWorld : function() {

        // Clear the HTML grid
        for (var s = 0; s < this.sides.length; s++) {
            this.sides[s].table.innerHTML = ''; 
        }
        this.sides = []
        this.generationElement.innerHTML = '0'; 

        // Rebuild the sides
        this.init(true); 
    },


    // Functions to run the next step, used both during Running and with Step button
    nextStep : function () {
        var start = (new Date).getMilliseconds();

        for (var s = 0; s < this.sides.length; s++) {
            this.sides[s].newWorld = this.arrayCopy(this.sides[s].world);

            for (var i = 0; i < this.sides[s].edge; i++) {
                for (var j = 0; j < this.sides[s].edge; j++) {
                    this.sides[s].checkState(i, j);
                }
            }

        }

        for (var s = 0; s < this.sides.length; s++) {
            this.sides[s].world = this.sides[s].newWorld
        }

        this.generationElement.innerHTML = this.generation++;

        if (this.running) {
            setTimeout(function() {game.nextStep(); }, this.waitTime);
        } else {
            if (this.clear) {
                this.clearWorld();
            }
        }

    },


    // Button handlers and other helper functions
    buttonRun : function(button) {
        this.running = !this.running;
        if (this.running) {
            this.nextStep();
        }
    },


    buttonClear : function () {
        if (this.running) {
            this.clear = true;
            this.running = ralse;
        } else {
            this.clearWorld();
        }
    },


    buttonNextStep : function() {
        if (!this.running)
        this.nextStep();
    },


    arrayCopy : function(src) {
        var x = src.length, y=src[0].length;
        var dest = [];
        for (var i = 0; i < x; i++) {
            dest[i] = [];
            for (var j=0; j < y; j++) {
                dest[i][j] = src[i][j];
            }
        }

        return dest;
    },


    addEvent : function(element, event, handler, capture) {
        if(/msie/i.test(navigator.userAgent)) {
            element.attachEvent('on' + event, handler);
        } else {
            element.addEventListener(event, handler, capture);
        }
    },


    cellMouseDownHandler : function(s, i, j, event) {
        this.sides[s].mouseDown = true;
        this.sides[s].changeCellState(i, j, event);
    },


    cellMouseUpHandler : function(s) {
        this.sides[s].mouseDown = false;
    },


    // Correspondence object to connect the six sides, sorted by direction then side. 
    // E.g., "u0" is the upwards edge of side 0
    // Not sure if there is a way to generalize this correspondence to other nets of the cube
    corr : {

        // Up direction
        "u0" : "u4",
        "u1" : "d0",
        "u2" : "r0",
        "u3" : "l0",
        "u4" : "u0",
        "u5" : "d3",

        // Down direction
        "d0" : "u1",
        "d1" : "r5",
        "d2" : "d5",
        "d3" : "u5",
        "d4" : "l5",
        "d5" : "d2",

        // Right direction
        "r0" : "u2",
        "r1" : "l2",
        "r2" : "l4",
        "r3" : "l1",
        "r4" : "l3",
        "r5" : "d1",

        // Left direction
        "l0" : "u3",
        "l1" : "r3",
        "l2" : "r1",
        "l3" : "r4",
        "l4" : "r2",
        "l5" : "d4"
    }
    
};



// Create a class for sides with all the methods needed
class Side {
    table = null;
    world = null;
    newWorld = null;
    cells = null;
    edge = 12;
    width = this.edge - 1;
    width_str = this.width.toString();
    colors = {
        dead : '#555',
        alive : '#90EE90',
    };
    mouseDown = false;
    constructor(id) {
        this.id = id;
    }


    // Function to generate the default grid. World and newWorld are the same right now
    initWorld() {
        this.world = [];
        this.newWorld = [];

        for (var i = 0; i < this.edge; i++) {
            this.world[i] = [];
            this.newWorld[i] = []; 

            for (var j = 0; j < this.edge; j++) {
                this.world[i][j] = false;
                this.newWorld[i][j] = false;
            }
        }
    }
    

    // Functions to change state -- used by the mouse handlers and by the game rules
    changeCellState(i, j) {
        this.world[i][j] = !this.world[i][j]; // Switcheroo
        if (this.world[i][j])
            this.changeCelltoAlive(i, j);
        else
            this.changeCelltoDead(i, j);
    }


    changeCelltoAlive(i, j) {
        this.cells[i][j].style.backgroundColor = this.colors.alive
    }


    changeCelltoDead(i, j) {
        this.cells[i][j].style.backgroundColor = this.colors.dead;
    }

    // Function to implement the "game of life" rules, based on how many neighbors each cell has
    checkState(i, j) {
        var neighbors = this.getNeighbors(i, j); 

        if (this.world[i][j]) {
            if (neighbors == 0 || neighbors == 1 || neighbors > 3)
                this.newWorld[i][j] = false;
        } else {
            if (neighbors == 3)
                this.newWorld[i][j] = true;
        }

        if (this.newWorld[i][j] != this.world[i][j]) {
            if (this.newWorld[i][j]) {
                this.changeCelltoAlive(i, j);
            } else {
                this.changeCelltoDead(i, j);
            }
        } else if (this.newWorld[i][j]) {
            this.changeCelltoAlive(i, j);
        }
    }
    

    // Function to count how many alive neighbors a cell has
    getNeighbors(i, j) {
        var neighbors = 0;

        // Check the 3 cells that are one above
        if (this.world[i - 1] != undefined) {
            neighbors +=
            (this.world[i - 1][j - 1] == undefined ? 0 : this.world[i - 1][j - 1] ? 1 : 0) +
            (this.world[i - 1][j] == undefined ? 0 : this.world[i - 1][j] ? 1 : 0) +
            (this.world[i - 1][j + 1] == undefined ? 0 : this.world[i - 1][j + 1] ? 1 : 0);
        }

        // Check the 2 cells that are in the same row
        neighbors +=
        (this.world[i][j - 1] == undefined ? 0 : this.world[i][j - 1] ? 1 : 0) +
        (this.world[i][j + 1] == undefined ? 0 : this.world[i][j + 1] ? 1 : 0);
        
        // Check the 3 cells that are below
        if (this.world[i + 1] != undefined) {
            neighbors +=
            (this.world[i + 1][j - 1] == undefined ? 0 : this.world[i + 1][j - 1] ? 1 : 0) +
            (this.world[i + 1][j] == undefined ? 0 : this.world[i + 1][j] ? 1 : 0) +
            (this.world[i + 1][j + 1] == undefined ? 0 : this.world[i + 1][j + 1] ? 1 : 0);
          }
        
        // Corner cases -- handled separately from edges
        // Note that corners only have 7 neighboring cells, not 8. Because math.
        if(i == 0 && j == 0 || i == this.width && j == this.width || i == 0 && j == this.width || i == this.width && j == 0) {
          
            var o = this.edgeCheck(this.id, "i", i.toString(), j)
            var o1 = this.edgeCheck(this.id, "j", j.toString(), i)

            // Check the two cells that are directly across on the opposite two sides. These definitely exist 
            neighbors +=
            (game.sides[+o[0]].world[+o[2]][+o[5]] ? 1 : 0) +
            (game.sides[+o1[0]].world[+o1[2]][+o1[5]] ? 1 : 0);

            // Check the 2 cells that are diagonal across on the opposite two sides.
            // Only 2 of these exist, but there are too many cases to specify which to check
            try {
                neighbors += (game.sides[+o[0]].world[+o[1]][+o[4]] ? 1 : 0);
            } catch (error) {}

            try {
                neighbors += (game.sides[+o[0]].world[+o[3]][+o[6]] ? 1 : 0);
            } catch (error) {}

            try {
                neighbors += (game.sides[+o1[0]].world[+o1[1]][+o1[4]] ? 1 : 0);
            } catch (error) {}

            try {
                neighbors += (game.sides[+o1[0]].world[+o1[3]][+o1[6]] ? 1 : 0);
            } catch (error) {}
            
        // Edge cases -- handled separately from corners
        } else if (i == 0 || i == this.width){
            var o = this.edgeCheck(this.id, "i", i, j)

            neighbors +=
            (game.sides[+o[0]].world[+o[1]][+o[4]] ? 1 : 0) +
            (game.sides[+o[0]].world[+o[2]][+o[5]] ? 1 : 0) +
            (game.sides[+o[0]].world[+o[3]][+o[6]] ? 1 : 0);
 
        } else if (j == 0 || j == this.width){
            var o = this.edgeCheck(this.id, "j", j, i)

            neighbors +=
            (game.sides[+o[0]].world[+o[1]][+o[4]] ? 1 : 0) +
            (game.sides[+o[0]].world[+o[2]][+o[5]] ? 1 : 0) +
            (game.sides[+o[0]].world[+o[3]][+o[6]] ? 1 : 0);

        } 

        return neighbors;
    }


    // Function to determine which neighboring cells are adjacent to edge and corner cells, used by getNeighbors()
    edgeCheck(side, i_or_j, start_or_end, i_or_j_value) {
        
        // Build string in form of "u1" for top edge of side 1
        let imax = "i" + this.width_str
        let jmax = "j" + this.width_str
        var direction = "";
        switch(i_or_j + start_or_end) {
            case "i0":
                direction = "u"
                break;
            case imax:
                direction = "d"
                break;
            case "j0":
                direction = "l"
                break;
            case jmax:
                direction = "r"
                break;
        }

        let old_side = direction + side.toString();
        let new_side = game.corr[old_side];

        // Handle sides that sort of "flip around"
        let exceptions = ["u0", "u4", "r0", "u2", "l5", "d4", "d5", "d2"]
        if (exceptions.includes(old_side)) {
            i_or_j_value = Math.abs(i_or_j_value - this.width)
        }

        let minus_one = i_or_j_value - 1;
        let plus_one = i_or_j_value + 1;

        // Handle corners here -- the output for a corner will now be 001 or 899
        if (minus_one < 0) {
            minus_one = "x";
        }
        if (plus_one > this.width){
            plus_one = "x";
        }
                
        // Return four pieces: new side id, x3 new i, and x3 new j 
        // For instance, suppose I want to check side 4 (0, 5)
        // Then I need to check side 1: (9, 4), (9, 5), and (9,6)
        // Example output: "1999456"
        // Then getNeigbhours() uses that

        switch(new_side[0]) {
            case "u":
                return [new_side[1], 0, 0, 0, minus_one, i_or_j_value, plus_one]
                break;
            case "d":
                return [new_side[1], this.width, this.width, this.width, minus_one, i_or_j_value, plus_one]
                break;
            case "l":
                return [new_side[1], minus_one, i_or_j_value, plus_one, 0, 0, 0]
                break;
            case "r":
                return [new_side[1], minus_one, i_or_j_value, plus_one, this.width, this.width, this.width]
                break;
        }
        
    }    

};



// Reference: I learned a lot of code from http://pmav.eu/stuff/javascript-game-of-life-v1.0/ 
// which is licensed under MIT liecense as follows:

/* Copyright (c) 2009 Pedro Verruma, http://pmav.eu

Permission is hereby granted, free of charge, to any person
obtaining a copy of this software and associated documentation
files (the "Software"), to deal in the Software without
restriction, including without limitation the rights to use,
copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the
Software is furnished to do so, subject to the following
conditions:

The above copyright notice and this permission notice shall be
included in all copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND,
EXPRESS OR IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES
OF MERCHANTABILITY, FITNESS FOR A PARTICULAR PURPOSE AND
NONINFRINGEMENT. IN NO EVENT SHALL THE AUTHORS OR COPYRIGHT
HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER LIABILITY,
WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING
FROM, OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR
OTHER DEALINGS IN THE SOFTWARE.
*/
