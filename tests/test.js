import {Complex} from './complex.js';

const a = new Complex(2, 3);
const b = new Complex(1, -4);

console.log(a.add(b).toString());
console.log(b.add(b).toString())
console.log(a.mul(a).toString())