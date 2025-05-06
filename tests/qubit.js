export class Qubit{
    constructor(){
        this.alpha = 1
        this.beta = 0
        this.state = [alpha, beta];
    }

    apply(gate){

    }

    reset(){
        this.alpha = 1
        this.beta = 0
    }

    getState(){
        return [this.alpha, this.beta]
    }

    toString(){
        
    }
}