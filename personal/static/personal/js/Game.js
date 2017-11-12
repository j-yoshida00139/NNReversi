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
    this.NONE  = 0;
    this.BLACK = 1;
    this.WHITE = 2;
    this.nextColor = this.BLACK;
    this.blackMove = [];
    this.whiteMove = [];
}

Game.prototype.init = function(){
    var upRow   = Math.floor((this.rows-1)/2);
    var leftCol = Math.floor((this.cols-1)/2);
    this.arrange = [];
    for (var i=0; i<this.rows; i++){
        this.arrange[i] = [];
        for (var j=0; j<this.cols; j++){
            this.clearPiece(i, j);
        }
    }
    this.putPiece(upRow  , leftCol  , this.BLACK);
    this.putPiece(upRow+1, leftCol  , this.WHITE);
    this.putPiece(upRow  , leftCol+1, this.WHITE);
    this.putPiece(upRow+1, leftCol+1, this.BLACK);
}

Game.prototype.clearPiece = function(row, col){
    this.arrange[row][col] = this.NONE;
}

Game.prototype.putPiece = function(row, col, color){    
    this.arrange[row][col] = color;
}

Game.prototype.canPutPiece = function(row, col, color){
    if(this.arrange[row][col]!==this.NONE){
        return false;
    }
    if(this.getTurnPieceList(row, col, color).length>0){
        return true;
    }
    return false;    
}

Game.prototype.storeMove = function(row, col, color){
    var currentArrange = unsharedCopy(this.arrange)
    if(color===this.BLACK){
        this.blackMove.push({arrange:currentArrange, row:row, col:col, color:color});
    }else{
        this.whiteMove.push({arrange:currentArrange, row:row, col:col, color:color});
    }
}

Game.prototype.isOutOfRange = function(row, col){
    if(row>=this.rows || col>=this.cols || row<0 || col<0){
        return true;
    }else{
        return false;
    }
};

Game.prototype.getScore = function(color){
    var counter = 0;
    for(var row=0; row<this.rows; row++){
        for(var col=0; col<this.cols; col++){
            if(this.arrange[row][col]===color){
                counter++;
            }
        }
    }
    return counter;
}

Game.prototype.getTurnPieceList = function(row, col, color){
    var turnPieceList = [];
    for(var i=0; i<directions.length; i++){
        var tmpTurnPieceList = this.getTurnPieceForDirect(row, col, color,  directions[i]['row'], directions[i]['col']);
        if(tmpTurnPieceList.length>0){
            for(var j=0; j<tmpTurnPieceList.length; j++){
                turnPieceList.push({row:tmpTurnPieceList[j]['row'], col:tmpTurnPieceList[j]['col']});
            }
        }
    }
    return turnPieceList;
};

Game.prototype.getTurnPieceForDirect = function(row, col, color, y, x){
    var turnPieceList = [];
    if(this.isOutOfRange(row+y, col+x)){
        return [];
    }
    var checkRow = row+y;
    var checkCol = col+x;
    if(this.arrange[checkRow][checkCol]===color || this.arrange[checkRow][checkCol]===this.NONE){
        return [];
    }
    var turnRows = [];
    var turnCols = [];
    turnRows.push(checkRow);
    turnCols.push(checkCol);
    checkRow += y;
    checkCol += x;
    while(!this.isOutOfRange(checkRow, checkCol)){
        if(this.arrange[checkRow][checkCol]===this.NONE){
            return [];
        }else if(this.arrange[checkRow][checkCol]===color){
            for (var i=0; i<turnRows.length; i++){
                turnPieceList.push({row:turnRows[i], col:turnCols[i]});
            }
            return turnPieceList;
        }
        turnRows.push(checkRow);
        turnCols.push(checkCol);
        checkRow += y;
        checkCol += x;
    }
    return turnPieceList;
}

Game.prototype.canPutPieceOnBoard = function(color){
    canPutList = this.getCanPutList(color);
    for(var i=0; i<canPutList.length; i++){
        if(canPutList[i]===1){
            return true;
        }
    }
    return false;
}

Game.prototype.getCanPutList = function(color){
    var canPutList = [];
    for(y=0; y<this.rows; y++){
        for(x=0; x<this.cols; x++){
            if(this.canPutPiece(y, x, color)){
                canPutList.push(1);
            }else{
                canPutList.push(0);
            }
        }
    }
    return canPutList;
}

Game.prototype.getWinnersData = function(){
    if( this.getScore(this.BLACK) > this.getScore(this.WHITE) ){
        return this.blackMove;
    }else{
        return this.whiteMove;
    }

}

function unsharedCopy(inList){
    returnList = [];
    inList.forEach(function(value){
        returnList.push(value.slice());
    });
    return returnList;
}
