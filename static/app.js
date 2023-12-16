let gameSeq=[];
let userSeq=[];


let btns = ["yellow", "red", "green", "purple"];

let started = false;
let level = 0;

let h2 = document.querySelector("h2");

document.addEventListener("keypress", function(){
    if(started == false){
        console.log("game started");
        started = true;
        levelUp();
    }
});

function gameFlash(btn){
    btn.classList.add("flash");
    setTimeout(function(){
        btn.classList.remove("flash");
    }, 250);
}

function userFlash(btn){
    btn.classList.add("userflash");
    setTimeout(function(){
        btn.classList.remove("userflash");
    }, 200);
}

function levelUp(){
    userSeq = [];
    level++;
    h2.innerText = `Level ${level}`;

    let randmIdx = Math.floor(Math.random() * 4);
    let randmColor = btns[randmIdx];
    let randmBtn = document.querySelector(`.${randmColor}`);
    // console.log(randmBtn);
    // console.log(randmColor);
    // console.log(randmIdx);
    gameSeq.push(randmColor);
    console.log(gameSeq);
    gameFlash(randmBtn);
}

function checkAns(idx){
    // console.log("Current level ", level);
    // let idx = level-1;

    if(userSeq[idx] === gameSeq[idx]){
        if(userSeq.length == gameSeq.length){
            setTimeout(levelUp, 1000);
        }
    } else {
        h2.innerHTML = `Game over!  Your score was <b> ${level}</b> <br> Press any key to start `;
        document.querySelector("body").style.backgroundColor = "rgb(165, 11, 11)";
        setTimeout(function () {
            document.querySelector("body").style.backgroundColor = "rgba(210, 192, 184, 0.811)";
        }, 450)
        reset(); 
    }
}

function btnPress(){
    // console.log(this);
    let btn = this;
    userFlash(btn);

    userColor = btn.getAttribute("id");
    userSeq.push(userColor);
    checkAns(userSeq.length-1); 
}

let allBtns = document.querySelectorAll(".btn");
for(btn of allBtns){
    btn.addEventListener("click", btnPress);
}

function reset(){
    started = false;
    gameSeq = [];
    userSeq = [];
    level = 0;
}