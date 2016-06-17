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
            this.clearPiece(context, i, j);
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

Game.prototype.canPutPieceOnBoard = function(color){
    for(y=0; y<this.rows; y++){
        for(x=0; x<this.cols; x++){
            if(this.canPutPiece(y, x, color)){
                return true;
            }
        }
    }
    return false;
}
