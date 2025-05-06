export class Complex{
    constructor(re, im = 0){
        this.re = re;
        this.im = im;
    }

    add(other){
        return new Complex(this.re + other.re, this.im + other.im);
    }

    mul(other){
        return new Complex(this.re * other.re - this.im * other.im, this.re * other.im + this.im * other.re);
    }

    conj(){
        return new Complex(this.re, -this.im);
    }

    abs(){
        return this.re**2 + this.im**2;
    }

    toString(){
        const imPart = this.im >= 0 ? `+${this.im}` : `${this.im}`;
        return `${this.re}${imPart}i`;
    }
}