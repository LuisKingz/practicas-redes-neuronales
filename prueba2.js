var _dev = {
    dead: false,
    init: () => {
        while(!this.dead){
            _dev.eat();
            _dev.code();
            // _dev.sleep()
        }
    },
    eat: () => {
        console.log("eating...");
    },
    code: () => {
        console.log("coding...");
    },
    sleep: () => {
        console.log("sleeping...");
    }
}.init()