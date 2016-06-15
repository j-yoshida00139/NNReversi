ROWS = 8;
COLS = 8;
NONE  = 0;
BLACK = 1;
WHITE = 2;
CANVAS_ID = 'reversi_board';
var eachHeight = 0;
var eachWidth = 0;
var nextColor = BLACK;
var game = new Game(ROWS, COLS);
var directions = [
    {row: 0, col: 1},
    {row:-1, col: 1},
    {row:-1, col: 0},
    {row:-1, col:-1},
    {row: 0, col:-1},
    {row: 1, col:-1},
    {row: 1, col: 0},
    {row: 1, col: 1}
]

onload = function () {
    var canvas = document.getElementById(CANVAS_ID);
    eachWidth = canvas.offsetWidth / COLS;
    eachHeight = canvas.offsetHeight / ROWS;
    var context = canvas.getContext('2d');

    game.init(context);
    
    document.getElementById(CANVAS_ID).addEventListener("click", function (e) {
        var mouseX = e.pageX;
        var mouseY = e.pageY;
        var rect = canvas.getBoundingClientRect();

        var positionX = rect.left + window.pageXOffset;
        var positionY = rect.top + window.pageYOffset;

        var offsetX = mouseX - positionX;
        var offsetY = mouseY - positionY;

        var row = Math.floor(offsetY / eachHeight);
        var col = Math.floor(offsetX / eachWidth );
        if(game.canPutPiece(row, col, nextColor)){
            game.putPiece(context, row, col, nextColor);
            game.turnPiece(context, row, col, nextColor);
            nextColor = (nextColor===BLACK)? WHITE:BLACK;
        }
    });
};
function putPiece(context, row, col, color) {
    var x = (col + 0.5) * eachWidth;
    var y = (row + 0.5) * eachHeight;
    var radius = Math.min(eachWidth, eachHeight) * 0.8 / 2;
    context.beginPath();
    context.fillStyle = (color===BLACK)? "#000" : "#fff";
    context.lineWidth = 1;
    context.arc(x, y, radius, 0, Math.PI * 2, false);
    context.fill();
    game.arrange[row][col] = color;
}
function clearPiece(context, row, col) {
    var xUpLeft = col * eachWidth;
    var yUpLeft = row * eachHeight;
    context.beginPath();
    context.strokeStyle = "#000";
    context.lineWidth = 1;
    context.fillStyle = "#080";
    context.strokeRect(xUpLeft, yUpLeft, eachWidth, eachHeight);
}

function Game(rows, cols){
    this.rows = rows;
    this.cols = cols;
}

Game.prototype.init = function(context){
    var upRow   = Math.floor((this.rows-1)/2);
    var leftCol = Math.floor((this.cols-1)/2);
    this.arrange = [];
    for (var i=0; i<this.rows; i++){
        this.arrange[i] = [];
        for (var j=0; j<this.cols; j++){
            game.clearPiece(context, i, j);
        }
    }
    this.putPiece(context, upRow  , leftCol  , BLACK);
    this.putPiece(context, upRow+1, leftCol  , WHITE);
    this.putPiece(context, upRow  , leftCol+1, WHITE);
    this.putPiece(context, upRow+1, leftCol+1, BLACK);
};

Game.prototype.clearPiece = function(context, row, col){
    this.arrange[row][col] = NONE;
    clearPiece(context, row, col);
}

Game.prototype.putPiece = function(context, row, col, color){
    this.arrange[row][col] = color;
    putPiece(context, row, col, color);
};

Game.prototype.canPutPiece = function(row, col, color){
    if(this.arrange[row][col]!==NONE){
        return false;
    }
    for(var i=0; i<directions.length; i++){
        if(this.canTurnPiece(row, col, color, directions[i]['row'], directions[i]['col'])){
            return true;
        }
    }
    return false;
};
Game.prototype.isOutOfRange = function(row, col){
    if(row>=this.rows || col>=this.cols || row<0 || col<0){
        return true;
    }else{
        return false;
    }
}
Game.prototype.canTurnPiece = function(row, col, color, y, x){
    if(this.isOutOfRange(row+y, col+x)){
        return false;
    }
    // Checking the color of next cell
    if(this.arrange[row+y][col+x]===color || this.arrange[row+y][col+x]===NONE){
        return false;
    }
    var checkRow = row+2*y;
    var checkCol = col+2*x;

    while(!this.isOutOfRange(checkRow, checkCol)){
        if(this.arrange[checkRow][checkCol]===color){
            return true;
        }
        checkRow += y;
        checkCol += x;        
    }
    return false;
};

Game.prototype.turnPiece = function(context, row, col, color){
    for(var i=0; i<directions.length; i++){
        if(this.turnPieceForDirect(context, row, col, color,  directions[i]['row'], directions[i]['col']));
    }
};

Game.prototype.turnPieceForDirect = function(context, row, col, color, y, x){
    if(this.isOutOfRange(row+y, col+x)){
        return false;
    }
    var checkRow = row+y;
    var checkCol = col+x;
    if(this.arrange[checkRow][checkCol]===color || this.arrange[checkRow][checkCol]===NONE){
        return false;
    }
    var turnRows = [];
    var turnCols = [];
    turnRows.push(checkRow);
    turnCols.push(checkCol);
    checkRow += y;
    checkCol += x;    
    while(!this.isOutOfRange(checkRow, checkCol)){
        if(this.arrange[checkRow][checkCol]===color){
            for (var i=0; i<turnRows.length; i++){
                this.putPiece(context, turnRows[i], turnCols[i], color);
            }
            return true;
        }
        turnRows.push(checkRow);
        turnCols.push(checkCol);
        checkRow += y;
        checkCol += x;
    }
    return false;
};
