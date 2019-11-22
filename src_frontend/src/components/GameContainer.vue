<template>
    <div>
        <p>
            {{ instructions }}
        </p>
        <game-board
                :checkers="checkers"
                :rowCount="rowCount"
                :colCount="colCount"
                :status="status"
                @drop="drop"
                @land="land"
        ></game-board>
        <p v-if="gameOver">
            {{ overMessage }}
            <a href="#" @click="reset">Play again</a>
        </p>
        <p v-else>
            {{ whoseTurn }}
        </p>
    </div>
</template>


<script>
    import Vue from 'vue';
    import GameBoard from '@/components/GameBoard.vue'
    import { OVER, PLAY, RED, BLACK, key, titleize, EMPTY, min, max } from '@/helpers/connect-four'

    export default {
        name: 'game-container',

        components: {
            GameBoard,
        },

        data() {
            return {
                checkers: {},
                isLocked: false,
                playerColor: RED,
                rowCount: 6,
                colCount: 7,
                status: PLAY,
                instructions: 'Click columns to add checkers',
                winner: undefined,
            };
        },

        created(){
            this.axios.get('http://localhost:8080/api/game/' + this.$route.params.id)
            .then((response) => {
                this.checkers = Object.assign({}, this.checkers,response.data )


                var counts = {};
                for (var prop in this.checkers)
                    counts[this.checkers[prop].color] = counts[this.checkers[prop].color]+1 || 1;

                if( ((counts[RED] > counts[BLACK]) && (this.playerColor === RED)) ||
                    ((counts[BLACK] > counts[RED]) && (this.playerColor === BLACK))
                ){
                    this.toggleColor()
                } else if (this.playerColor === BLACK) { // The BLACK player is the AI, so the user should use his color!
                    this.toggleColor()
                }

            })
        },

        computed: {
            overMessage() {
                if (this.winner) {
                    return `${titleize(this.winner.color)} wins!`;
                } else {
                    return `It's a draw!`;
                }
            },

            moves() {
                return Object.values(this.checkers);
            },

            whoseTurn() {
                return `${titleize(this.playerColor)} goes ${this.moves.length === 0 ? 'first' : 'next'}`;
            },

            gameOver() {
                return this.status === OVER;
            },
        },

        methods: {
            key,

            reset() {
                this.startGame()
                /*
                this.winner = undefined;
                this.isLocked = false;
                this.status = PLAY;
                this.checkers = {};
                */
            },

            toggleColor() {
                if (this.playerColor === RED) {
                    this.playerColor = BLACK;
                } else {
                    this.playerColor = RED;
                }
            },

            setChecker({ row, col }, attrs = {}) {
                const checker = this.getChecker({ row, col });
                return Vue.set(this.checkers, key(row, col), { ...checker, ...attrs });
            },

            getChecker({ row, col }) {
                return this.checkers[key(row, col)] || { row, col, color: 'empty' };
            },

            drop({ col, row }) {
                if (this.isLocked) return;

                this.isLocked = true;
                const color = this.playerColor;

                this.moveIsValidAndGetAIMove({row, col, color})
                .then(response => {
                    this.setChecker({ row, col }, { color });
                    this.checkForDraw();
                    this.checkForWinFrom({ row, col });
                    if(this.winner) return;

                    let moveOfAI = { row: response.data.row , col: response.data.col };
                    this.setChecker(moveOfAI, { color: BLACK });
                    this.checkForDraw() || this.checkForWinFrom(moveOfAI);

                }).catch(error => {
                    this.isLocked = false;
                    this.notifyNotValidMove(`${error.response.status} - ${error.response.statusText}`);
                })
            },

            land() {
                if (this.isDraw) return this.displayDraw();

                if (this.winner) {
                    this.displayWin(this.winner);
                } else {
                    this.isLocked = false;
                }
            },

            checkForDraw() {
                this.isDraw = Object.keys(this.checkers).length === this.rowCount * this.colCount;
            },

            getWinner(...segment) {
                if (segment.length !== 4) return false;
                const checkers = segment.map(([row, col]) => this.getChecker({row, col}));
                const color = checkers[0].color;
                if (color === EMPTY) return false;
                if (checkers.every(c => c.color === color)) return { color, checkers };
                return false;
            },

            checkHorizontalSegments({ focalRow, minCol, maxCol }) {
                for (let row = focalRow, col = minCol; col <= maxCol; col++) {
                    const winner = this.getWinner([row, col], [row, col+1], [row, col+2], [row, col+3]);
                    if (winner) return winner;
                }
            },

            // eslint-disable-next-line no-unused-vars
            checkVerticalSegments({ focalRow, focalCol, minRow, maxRow }) {
                for (let col = focalCol, row = minRow; row <= focalRow; row++) {
                    const winner = this.getWinner([row, col], [row+1, col], [row+2, col], [row+3, col]);
                    if (winner) return winner;
                }
            },

            checkForwardSlashSegments({ focalRow, focalCol, minRow, minCol, maxRow, maxCol }) {
                const startForwardSlash = (row, col) => {
                    while(row > minRow && col > minCol) { row--; col--; }
                    return [row, col]
                }
                for (let [row, col] = startForwardSlash(focalRow, focalCol); row <= maxRow && col <= maxCol; row++, col++) {
                    const winner = this.getWinner([row, col], [row+1, col+1], [row+2, col+2], [row+3, col+3]);
                    if (winner) return winner;
                }
            },

            checkBackwardSlashSegments({ focalRow, focalCol, minRow, minCol, maxRow, maxCol }) {
                const startBackwardSlash = (row, col) => {
                    while(row < maxRow && col > minCol) { row++; col--; }
                    return [row, col]
                }
                for (let [row, col] = startBackwardSlash(focalRow, focalCol); row >= minRow && col <= maxCol; row--, col++) {
                    const winner = this.getWinner([row, col], [row-1, col+1], [row-2, col+2], [row-3, col+3]);
                    if (winner) return winner;
                }
            },

            checkForWinFrom(lastChecker) {
                if (!lastChecker) return;
                const { row: focalRow, col: focalCol } = lastChecker;
                const minCol = min(focalCol);
                const maxCol = max(focalCol, this.colCount-1);
                const minRow = min(focalRow);
                const maxRow = max(focalRow, this.rowCount-1);
                const coords = { focalRow, focalCol, minRow, minCol, maxRow, maxCol };

                this.winner = this.checkHorizontalSegments(coords) ||
                    this.checkVerticalSegments(coords) ||
                    this.checkForwardSlashSegments(coords) ||
                    this.checkBackwardSlashSegments(coords);
            },

            displayDraw() {
                this.status = OVER;
            },

            displayWin(winner) {
                this.winner = winner;
                this.status = OVER;
                this.winner.checkers.forEach((checker) => {
                    this.setChecker(checker, {isWinner: true});
                });
                if(winner.color === RED){
                    this.$swal(`You won!`, "Congratulation!", 'success');
                } else {
                    this.$swal(`The AI won! &#128531;`, "Next time you will be better!", 'error');
                }
            },

            startGame(){
                this.axios.get('http://localhost:8080/api/game/start')
                    .then((response) => {
                        this.$router.push({
                            name: 'Game',
                            params: { id: response.data.id }
                        })
                    }).catch(error => {
                    this.$swal("I couldn't create a new game!", `${error.response.status} - ${error.response.statusText}`, 'error');
                })
            },

            moveIsValidAndGetAIMove(attr){
                return this.axios.post(`http://localhost:8080/api/${this.$route.params.id}/move`, attr)

            },

            notifyNotValidMove(msg){
                this.$swal("This is not a valid move!", msg, 'error');
            },

        },



    }
</script>