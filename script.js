class OthelloGame {
    constructor() {
        this.board = Array(8).fill().map(() => Array(8).fill(null));
        this.currentPlayer = 'black';
        this.gameOver = false;
        this.passCount = 0;
        
        this.initializeBoard();
        this.createBoard();
        this.updateDisplay();
        this.setupEventListeners();
    }

    initializeBoard() {
        // 初期配置
        this.board[3][3] = 'white';
        this.board[3][4] = 'black';
        this.board[4][3] = 'black';
        this.board[4][4] = 'white';
    }

    createBoard() {
        const gameBoard = document.getElementById('game-board');
        gameBoard.innerHTML = '';

        for (let row = 0; row < 8; row++) {
            for (let col = 0; col < 8; col++) {
                const cell = document.createElement('div');
                cell.className = 'cell';
                cell.dataset.row = row;
                cell.dataset.col = col;
                
                if (this.board[row][col]) {
                    const piece = document.createElement('div');
                    piece.className = `game-piece ${this.board[row][col]}`;
                    cell.appendChild(piece);
                }
                
                gameBoard.appendChild(cell);
            }
        }
    }

    setupEventListeners() {
        const gameBoard = document.getElementById('game-board');
        const resetBtn = document.getElementById('reset-btn');
        const passBtn = document.getElementById('pass-btn');

        gameBoard.addEventListener('click', (e) => {
            if (this.gameOver) return;
            
            const cell = e.target.closest('.cell');
            if (!cell) return;

            const row = parseInt(cell.dataset.row);
            const col = parseInt(cell.dataset.col);

            if (this.isValidMove(row, col)) {
                this.makeMove(row, col);
            }
        });

        resetBtn.addEventListener('click', () => {
            this.resetGame();
        });

        passBtn.addEventListener('click', () => {
            this.passTurn();
        });
    }

    isValidMove(row, col) {
        if (this.board[row][col] !== null) return false;

        const directions = [
            [-1, -1], [-1, 0], [-1, 1],
            [0, -1],           [0, 1],
            [1, -1],  [1, 0],  [1, 1]
        ];

        for (const [dr, dc] of directions) {
            if (this.checkDirection(row, col, dr, dc)) {
                return true;
            }
        }
        return false;
    }

    checkDirection(row, col, dr, dc) {
        const opponent = this.currentPlayer === 'black' ? 'white' : 'black';
        let r = row + dr;
        let c = col + dc;
        let foundOpponent = false;

        while (r >= 0 && r < 8 && c >= 0 && c < 8) {
            if (this.board[r][c] === null) return false;
            if (this.board[r][c] === opponent) {
                foundOpponent = true;
            } else if (this.board[r][c] === this.currentPlayer) {
                return foundOpponent;
            }
            r += dr;
            c += dc;
        }
        return false;
    }

    makeMove(row, col) {
        this.board[row][col] = this.currentPlayer;
        this.flipPieces(row, col);
        this.passCount = 0;
        this.currentPlayer = this.currentPlayer === 'black' ? 'white' : 'black';
        this.updateDisplay();
        this.checkGameOver();
    }

    flipPieces(row, col) {
        const directions = [
            [-1, -1], [-1, 0], [-1, 1],
            [0, -1],           [0, 1],
            [1, -1],  [1, 0],  [1, 1]
        ];

        for (const [dr, dc] of directions) {
            this.flipDirection(row, col, dr, dc);
        }
    }

    flipDirection(row, col, dr, dc) {
        const opponent = this.currentPlayer === 'black' ? 'white' : 'black';
        const piecesToFlip = [];
        let r = row + dr;
        let c = col + dc;

        while (r >= 0 && r < 8 && c >= 0 && c < 8) {
            if (this.board[r][c] === null) return;
            if (this.board[r][c] === opponent) {
                piecesToFlip.push([r, c]);
            } else if (this.board[r][c] === this.currentPlayer) {
                // 反転する石を更新
                piecesToFlip.forEach(([fr, fc]) => {
                    this.board[fr][fc] = this.currentPlayer;
                });
                return;
            }
            r += dr;
            c += dc;
        }
    }

    getValidMoves() {
        const validMoves = [];
        for (let row = 0; row < 8; row++) {
            for (let col = 0; col < 8; col++) {
                if (this.isValidMove(row, col)) {
                    validMoves.push([row, col]);
                }
            }
        }
        return validMoves;
    }

    updateDisplay() {
        this.createBoard();
        this.highlightValidMoves();
        this.updateScore();
        this.updateCurrentPlayer();
        this.updateGameStatus();
    }

    highlightValidMoves() {
        if (this.gameOver) return;

        const validMoves = this.getValidMoves();
        const cells = document.querySelectorAll('.cell');

        cells.forEach(cell => {
            cell.classList.remove('valid-move');
        });

        validMoves.forEach(([row, col]) => {
            const cell = document.querySelector(`[data-row="${row}"][data-col="${col}"]`);
            if (cell) {
                cell.classList.add('valid-move');
            }
        });

        // パスボタンの表示制御
        const passBtn = document.getElementById('pass-btn');
        if (validMoves.length === 0) {
            passBtn.style.display = 'inline-block';
        } else {
            passBtn.style.display = 'none';
        }
    }

    updateScore() {
        let blackCount = 0;
        let whiteCount = 0;

        for (let row = 0; row < 8; row++) {
            for (let col = 0; col < 8; col++) {
                if (this.board[row][col] === 'black') blackCount++;
                if (this.board[row][col] === 'white') whiteCount++;
            }
        }

        document.getElementById('black-score').textContent = blackCount;
        document.getElementById('white-score').textContent = whiteCount;
    }

    updateCurrentPlayer() {
        const currentPlayerElement = document.getElementById('current-player');
        currentPlayerElement.textContent = this.currentPlayer === 'black' ? '黒' : '白';
        currentPlayerElement.style.color = this.currentPlayer === 'black' ? '#000' : '#666';
    }

    updateGameStatus() {
        const statusElement = document.getElementById('game-status');
        
        if (this.gameOver) {
            const blackCount = parseInt(document.getElementById('black-score').textContent);
            const whiteCount = parseInt(document.getElementById('white-score').textContent);
            
            if (blackCount > whiteCount) {
                statusElement.textContent = '黒の勝利！';
                statusElement.className = 'game-status winner';
            } else if (whiteCount > blackCount) {
                statusElement.textContent = '白の勝利！';
                statusElement.className = 'game-status winner';
            } else {
                statusElement.textContent = '引き分け！';
                statusElement.className = 'game-status tie';
            }
        } else {
            statusElement.textContent = '';
            statusElement.className = 'game-status';
        }
    }

    passTurn() {
        this.passCount++;
        this.currentPlayer = this.currentPlayer === 'black' ? 'white' : 'black';
        this.updateDisplay();
        this.checkGameOver();
    }

    checkGameOver() {
        const validMoves = this.getValidMoves();
        
        if (validMoves.length === 0) {
            if (this.passCount >= 1) {
                this.gameOver = true;
                this.updateGameStatus();
            } else {
                this.passTurn();
            }
        }
    }

    resetGame() {
        this.board = Array(8).fill().map(() => Array(8).fill(null));
        this.currentPlayer = 'black';
        this.gameOver = false;
        this.passCount = 0;
        
        this.initializeBoard();
        this.updateDisplay();
    }
}

// ゲーム開始
document.addEventListener('DOMContentLoaded', () => {
    new OthelloGame();
});