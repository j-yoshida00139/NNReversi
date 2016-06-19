ROWS = 8;
COLS = 8;
NONE  = 0;
BLACK = 1;
WHITE = 2;
BLACK_COLOR = "#000";
WHITE_COLOR = "#fff";
GREEN_COLOR = "#080";
CANVAS_ID = 'reversi_board';
var eachHeight = 0;
var eachWidth = 0;
var game = new Game(ROWS, COLS);
CONTEXT_GLOBAL = null;

onload = function () {
    var canvas = document.getElementById(CANVAS_ID);
    var context = canvas.getContext('2d');
    CONTEXT_GLOBAL = context;
    eachWidth = canvas.offsetWidth / COLS;
    eachHeight = canvas.offsetHeight / ROWS;

    game.init(context);
    
    document.getElementById(CANVAS_ID).addEventListener("click", function (e) {
        var rect = canvas.getBoundingClientRect();

        var positionX = rect.left + window.pageXOffset;
        var positionY = rect.top + window.pageYOffset;

        var offsetX = e.pageX - positionX;
        var offsetY = e.pageY - positionY;

        var row = Math.floor(offsetY / eachHeight);
        var col = Math.floor(offsetX / eachWidth );

        if(game.canPutPiece(row, col, game.nextColor)){
            game.putPiece(context, row, col, game.nextColor);
            game.turnPiece(context, row, col, game.nextColor);
            game.nextColor = (game.nextColor===BLACK)? WHITE:BLACK;
            runAjax();
        }
        if(!game.canPutPieceOnBoard(game.nextColor)){
            game.nextColor = (game.nextColor===BLACK)? WHITE:BLACK;
            if(!game.canPutPieceOnBoard(game.nextColor)){
                window.alert("終わり!");
            }
        }
        $('#turn').html(game.nextColor===BLACK? 'Black':'White')
    });
};

function putPiece(context, row, col, color) {
    var x = (col + 0.5) * eachWidth;
    var y = (row + 0.5) * eachHeight;
    var radius = Math.min(eachWidth, eachHeight) * 0.8 / 2;
    context.beginPath();
    context.fillStyle = (color===BLACK)? BLACK_COLOR : WHITE_COLOR;
    context.lineWidth = 1;
    context.arc(x, y, radius, 0, Math.PI * 2, false);
    context.fill();
    game.arrange[row][col] = color;
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

function runAjax() {
    var arrangeJson = JSON.stringify(game.arrange);
    $.ajax({
        type: "POST",
        url: "/ajax/test/",
        dataType: "json",
        data: {
            "color":game.nextColor,
            "arrange": arrangeJson
        },
        success: function(data) {
            setTimeout (function () {
                row = data["row"];
                col = data["col"];
                game.putPiece(CONTEXT_GLOBAL, row, col, game.nextColor);
                game.turnPiece(CONTEXT_GLOBAL, row, col, game.nextColor);
                game.nextColor = (game.nextColor===BLACK)? WHITE:BLACK;
            }, 1000)
        }
    });
}

