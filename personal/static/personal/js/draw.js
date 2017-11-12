ROWS = 8;
COLS = 8;
BLACK_COLOR = "#000";
WHITE_COLOR = "#fff";
GREEN_COLOR = "#080";
CANVAS_ID = 'reversi_board';
var eachHeight = 0;
var eachWidth = 0;
var game = new Game(ROWS, COLS);
var counter = 4;

onload = function () {

    var canvas = document.getElementById(CANVAS_ID);
    var context = canvas.getContext('2d');
    eachWidth = canvas.offsetWidth / COLS;
    eachHeight = canvas.offsetHeight / ROWS;

    game.init();
    var upRow   = Math.floor((ROWS-1)/2);
    var leftCol = Math.floor((COLS-1)/2);
    for (var i=0; i<ROWS; i++){
        for (var j=0; j<COLS; j++){
            clearPiece(context, i, j);
        }
    }
    putPiece(context, upRow  , leftCol  , game.BLACK);
    putPiece(context, upRow+1, leftCol  , game.WHITE);
    putPiece(context, upRow  , leftCol+1, game.WHITE);
    putPiece(context, upRow+1, leftCol+1, game.BLACK);
    
    document.getElementById(CANVAS_ID).addEventListener("click", function (e) {
        var rect = canvas.getBoundingClientRect();

        var positionX = rect.left + window.pageXOffset;
        var positionY = rect.top + window.pageYOffset;

        var offsetX = e.pageX - positionX;
        var offsetY = e.pageY - positionY;

        var row = Math.floor(offsetY / eachHeight);
        var col = Math.floor(offsetX / eachWidth );

        if(game.canPutPiece(row, col, game.nextColor)){
            game.storeMove(row, col, game.nextColor);
            putPiece(context, row, col, game.nextColor);
            turnPieceList = game.getTurnPieceList(row, col, game.nextColor);
            turnPiece(context, turnPieceList, game.nextColor);
            $('#countBlack').html(game.getScore(game.BLACK));
            $('#countWhite').html(game.getScore(game.WHITE));
            goNextTurn(context);
            counter++;
        }
        $('#turn').html(game.nextColor===game.BLACK? 'Black':'White')
    });
};

function goNextTurn(context){
    game.nextColor = (game.nextColor===game.BLACK)? game.WHITE:game.BLACK;
    if(game.canPutPieceOnBoard(game.nextColor)){
        if(game.nextColor===game.WHITE){
            moveByNN(context);
        }
        return;
    }
    // Case that the next user could not put any pieces
    game.nextColor = (game.nextColor===game.BLACK)? game.WHITE:game.BLACK;
    if(game.canPutPieceOnBoard(game.nextColor)){
        var colorStr = game.nextColor===game.BLACK? "黒":"白";
        window.alert("次のプレイヤーが置ける場所がないので、次も" + colorStr + "の番です");
        if(game.nextColor===game.WHITE){
            moveByNN(context);
        }
        return;
    }
    // Case that both users could not put any pieces
    window.alert("終わり!");
    var winnersData = game.getWinnersData();
    sendWinnersData(winnersData);
}

function turnPiece(context, turnPieceList, color){
    for(var i=0; i<turnPieceList.length; i++){
        putPiece(context, turnPieceList[i]["row"], turnPieceList[i]["col"], color);
    }
}

function putPiece(context, row, col, color) {
    drawPiece(context, row, col, color);
    game.putPiece(row, col, color);
}

function drawPiece(context, row, col, color){
    var x = (col + 0.5) * eachWidth;
    var y = (row + 0.5) * eachHeight;
    var radius = Math.min(eachWidth, eachHeight) * 0.8 / 2;
    context.beginPath();
    context.fillStyle = (color===game.BLACK)? BLACK_COLOR : WHITE_COLOR;
    context.lineWidth = 1;
    context.arc(x, y, radius, 0, Math.PI * 2, false);
    context.fill();    
}

function clearPiece(context, row, col) {
    var xUpLeft = col * eachWidth;
    var yUpLeft = row * eachHeight;
    context.beginPath();
    context.strokeStyle = BLACK_COLOR;
    context.lineWidth = 1;
    context.fillStyle = GREEN_COLOR;
    context.strokeRect(xUpLeft, yUpLeft, eachWidth, eachHeight);
}

function moveByNN(context) {
    var arrangeJson = JSON.stringify(game.arrange);
    var canPutListJson = JSON.stringify(game.getCanPutList(game.nextColor));
    $.ajax({
        type: "POST",
        url: "/ajax/nextMove/",
        dataType: "json",
        data: {
            "color"     : game.nextColor,
            "arrange"   : arrangeJson,
            "canPutList": canPutListJson
        },
        success: function(data) {
            setTimeout (function () {
                row = data["row"];
                col = data["col"];
                game.storeMove(row, col, game.nextColor);
                putPiece(context, row, col, game.nextColor);
                turnPieceList = game.getTurnPieceList(row, col, game.nextColor);
                turnPiece(context, turnPieceList, game.nextColor);
                $('#countBlack').html(game.getScore(game.BLACK));
                $('#countWhite').html(game.getScore(game.WHITE));
                goNextTurn(context);
                counter++;
                $('#counter').html(counter);
            }, 300);
        }
    });
}

function sendWinnersData(winnersData) {
    var winnersDataJson = JSON.stringify(winnersData);
    $.ajax({
        type: "POST",
        url: "/ajax/storeWinnersData/",
        dataType: "json",
        data: {
            "winnersData"     : winnersDataJson
        },
        success: function(data) {
        }
    });
}
