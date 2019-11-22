const range = num => [...Array(num).keys()];

const key = (row, col) => `${row}${col}`;
const cssUrl = id => `url(#${id})`;
const titleize = text => text[0].toUpperCase() + text.slice(1, text.length)
const min = num => Math.max(num - 3, 0);
const max = (num, max) => Math.min(num + 3, max);

const RED = 'red';
const BLACK = 'black';
const GREEN = 'green';
const EMPTY = 'empty';
const OVER = 'over';
const PLAY = 'play';

export { range, key, cssUrl, titleize, min, max, RED, BLACK, EMPTY, GREEN, OVER, PLAY };