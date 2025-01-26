import kaplay from "kaplay";
import battle from "./battle";
import { Entity } from "./entity";

const k = kaplay({
    width: 480,
    height: 480
});

k.loadRoot("./"); // A good idea for Itch.io publishing later
k.loadSprite("player", "sprites/player.png");
k.loadSprite("bandit_leader", "sprites/bandit_leader.png");
k.loadSprite("beach", "sprites/beach.png");
loadFont("jersey", "fonts/jersey.ttf");
k.onClick(() => k.addKaboom(k.mousePos()));


const createMessage = (text, duration=1) => {
    return k.add([
        k.text(text, { font: 'jersey' }),
        k.pos(k.center()),
        k.anchor('center'),
        k.opacity(1),
        k.lifespan(duration, { fade: 0.5 }),
    ])
}

const center = k.center();
const beach_backgroundd = k.add([
    k.sprite('beach'),
    k.scale(k.vec2(2,2))
])

let regionCount = 1
const regionName = k.add([
    k.text('Beach 1/25', { font: 'jersey', size: 24 }),
    k.pos(16, 16),
    k.anchor('topleft')
])
const updateRegionCount = (count) => {
    regionCount = count
    regionName.text = `Beach ${regionCount}/25`
}


let battleActions = battle.randomBattle();
let battleStep = 0;

let player = null;
let enemy = null;

const actions = {
    battleStart(playerData, enemyData) {
        if(player) player.die();
        player = new Entity(k, center.x, center.y+125, 'player', playerData);
        
        if(enemy) enemy.die();
        enemy = new Entity(k, center.x, center.y-125, enemyData.name, enemyData);
    },
    damagePlayer(damage) {
        player.damage(k, damage)
    },
    damageEnemy(damage) {
        enemy.damage(k, damage)
    },
    winPlayer() {
        createMessage('Player win');
        enemy.die();
    },
    winEnemy() {
        createMessage('Enemy win');
        player.die();
    },
    draw() {
        createMessage('Draw');
    }
}

k.onUpdate(() => {
    if(enemy != null) {
        enemy.updateLifebar('bar');
    }
    if(player != null) {
        player.updateLifebar('foo');
    }
});


const buttonExplore = document.querySelector('button#explore')

buttonExplore.addEventListener('click', () => {
    if(battleStep >= battleActions.length) {
        createMessage('Exploring...');
        battleActions = battle.randomBattle();
        battleStep = 0;
    } else {
        createMessage('Wait!');
    }
    updateRegionCount(regionCount+1)
})

setInterval(() => {
    if(battleStep < battleActions.length) {
        buttonExplore.setAttribute('disabled', true);
        buttonExplore.innerHTML = 'Exploring...';
        console.log(battleActions[battleStep])
        const actioName = battleActions[battleStep].action;
        const args = battleActions[battleStep].args;
        actions[actioName](...args);
        battleStep++;
    } else {
        buttonExplore.removeAttribute('disabled')
        buttonExplore.innerHTML = 'Explore';
    }
}, 500)