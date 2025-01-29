import kaplay from "kaplay";
import battle from "./battle";
import { Entity } from "./entity";

const k = kaplay({
    width: 480,
    height: 480
});

k.loadRoot("./"); // A good idea for Itch.io publishing later
k.loadSprite("player", "sprites/player.png");

// Beach Sprites
k.loadSprite("bandit_leader", "sprites/beach/bandit_leader.png");
k.loadSprite("pirate", "sprites/beach/pirate.png");
k.loadSprite("beached_bucaneer", "sprites/beach/beached_bucaneer.png");
k.loadSprite("treasure_chest", "sprites/beach/treasure_chest.png");
k.loadSprite("dreadstump_the_pirate_king", "sprites/beach/dreadstump_the_pirate_king.png");
k.loadSprite("beach", "sprites/beach/beach.png", {
    sliceX: 5,
    sliceY: 5
});

// MidPlains Sprites
k.loadSprite("mid_plains", "sprites/mid_plains/mid_plains.png", {
    sliceX: 5,
    sliceY: 5
});
k.loadSprite("big_green_slime", "sprites/mid_plains/big_green_slime.png");
k.loadSprite("earth_golem", "sprites/mid_plains/earth_golem.png");
k.loadSprite("fire_sprite", "sprites/mid_plains/fire_sprite.png");
k.loadSprite("swarm", "sprites/mid_plains/swarm.png");
k.loadSprite("shambling_sludge", "sprites/mid_plains/shambling_sludge.png");

loadFont("jersey", "fonts/jersey.ttf");

const center = k.center();

const createMessage = (text, duration=1, infinite=false) => {
    const width = text.length * 22;
    const components = [
        k.rect(16 + width, 48),
        k.color(k.rgb(0,0,0)),
        k.opacity(0.7),
        k.pos(center.x, center.y+( infinite ? 0 : 32 )),
        k.anchor('center'),
        k.z(100)
    ]
    if(!infinite) {
        components.push(k.move(k.vec2(0,-1), 50))
        components.push(k.lifespan(duration, { fade: 0.5 }))
    }
    const textBackground = k.add(components)
    textBackground.add([
        k.text(text, { font: 'jersey' }),
        k.anchor('center')
    ])
    return textBackground;
}

const createBackground = ({ spriteName }) => {
    k.addLevel([
        "1111111111",
        "1111111111",
        "1111111111",
        "1111111111",
        "1111111111",
        "1111111111",
        "1111111111",
        "1111111111",
        "1111111111",
        "1111111111",
    ], {
        tileHeight: 256/5,
        tileWidth: 256/5,
        tiles: {
            "1": () => [
                k.sprite(spriteName, { frame: 1})
            ]
        }
    })
}



const updateInfo = ({ level, exp, dex, att, def, next, gold}) => {
    document.querySelector('#attribute-level').innerHTML = level;
    document.querySelector('#attribute-exp').innerHTML = `${exp}/${next}`;
    document.querySelector('#attribute-dex').innerHTML = dex;
    document.querySelector('#attribute-att').innerHTML = att;
    document.querySelector('#attribute-def').innerHTML = def;
    document.querySelector('input#gold').value = gold;
}

let battleActions = []
let battleStep = 0;

let player = null;
let enemy = null;

const createRegionInfo = ({ name, level, maxLevel }) => {
    const regionWindow = k.add([
        k.rect(0, 32),
        k.pos(12, 12),
        k.color(k.rgb(0,0,0)),
        k.opacity(0.7),
        k.z(10)
    ])
    const regionLabel = regionWindow.add([
        k.text('', { font: 'jersey', size: 24 }),
        k.pos(6, 4),
        k.anchor('topleft')
    ])
    regionLabel.text = `${name} ${level}/${maxLevel}`
    regionWindow.width = regionLabel.width + 16
}

const actions = {
    BATTLE_START({ playerData, enemyData, regionData }) {
        k.destroyAll();
        createBackground(regionData);
        createRegionInfo(regionData);
        updateInfo(playerData)
        player = new Entity(k, center.x, center.y+125, 'player', playerData);
        enemy = new Entity(k, center.x, center.y-125, enemyData.name, enemyData);

    },
    BATTLE_ENEMY_ATTACK({ playerData, enemyData, damage }) {
        enemy.emmitAttack(k)
        player.updateMP(k, playerData.mp)
        enemy.updateMP(k, enemyData.mp)
        k.wait(0.5, () => {
            player.damage(k, damage)
        })
    },
    BATTLE_PLAYER_ATTACK({ playerData, enemyData, damage }) {
        player.emmitAttack(k)
        player.updateMP(k, playerData.mp)
        enemy.updateMP(k, enemyData.mp)
        k.wait(0.5, () => {
            enemy.damage(k, damage)
        })

    },
    BATTLE_WIN({ playerData }) {
        updateInfo(playerData)
        enemy.die(k);
    },
    BATTLE_DIE() {
        player.die(k);
        // document.querySelector('#auto-explore').checked = false;
    },
    MESSAGE({ content }) {
        createMessage(content);
    }
}

const buttonExplore = document.querySelector('button#explore')

buttonExplore.addEventListener('click', () => {
    if(battleStep >= battleActions.length) {
        createMessage('Exploring...');
        k.wait(0.5, () => {
            const region = document.querySelector('#region').value;
            battleActions = battle.randomBattle(region);
            battleStep = 0;
        })
    } else {
        createMessage('Wait!');
    }
})

document.querySelector('button#restart-progress').addEventListener('click', () => {
    localStorage.clear();
    location.reload();
});

k.add([
    k.rect(480,480),
    k.color(k.rgb(0,0,0))
])

createMessage('Start Exploring', 1, true);

const battleExecuteStep = () => {
    let duration = .5;
    if(battleStep < battleActions.length) {
        buttonExplore.setAttribute('disabled', true);
        buttonExplore.innerHTML = 'Exploring';
        const actionName = battleActions[battleStep].action;
        const actionArgs = battleActions[battleStep].args || {};
        const actionDuration = battleActions[battleStep].duration || duration;
        duration = actionDuration;
        actions[actionName](actionArgs);
        battleStep++;
    } else {
        buttonExplore.removeAttribute('disabled')
        buttonExplore.innerHTML = 'Explore';
        if(document.querySelector('#auto-explore').checked) {
            buttonExplore.click();
        }
    }
    k.wait(duration, () => {
        battleExecuteStep();
    })
}

k.wait(1, () => {
    battleExecuteStep();
})