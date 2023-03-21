var dead = false;

var eat = () => {
    console.log("Comer");
} 
var code = () => {
    console.log("Programar");
}
var sleep = () => {
    console.log("Dormir");
}

while (!dead) {
    eat();
    code();
    // sleep()
}
