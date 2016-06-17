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
var nextColor = BLACK;
var game = new Game(ROWS, COLS);


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
        if(!game.canPutPieceOnBoard(nextColor)){
            nextColor = (nextColor===BLACK)? WHITE:BLACK;
            if(!game.canPutPieceOnBoard(nextColor)){
                window.alert("終わり!");
            }
        }
        $('#turn').html(nextColor===BLACK? 'Black':'White')
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
            "color":nextColor,
            "arrange": arrangeJson
        },
        success: function(data) {
            alert(data);
        }
    });
}

