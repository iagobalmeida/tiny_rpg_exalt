import battle from "./battle";
import k from "./kaplayMain";
import { createBackground, createDamageText, createEntity, createMessage, createProjectile, createRegionInfo } from "./kaplayUtils";

createBackground();

const center = k.center();

const updateInfo = ({ level, exp, dex, att, def, next}) => {
    document.querySelector('#attribute-level').innerHTML = level;
    document.querySelector('#attribute-exp').innerHTML = `${exp}/${next}`;
    document.querySelector('#attribute-dex').innerHTML = dex;
    document.querySelector('#attribute-att').innerHTML = att;
    document.querySelector('#attribute-def').innerHTML = def;
}

let battleActions = []
let battleStep = 0;

let player = null;
let enemy = null;

const actions = {
    BATTLE_START({ playerData, enemyData, regionData }) {
        k.destroyAll();
        createBackground(regionData.spriteName);
        createRegionInfo(regionData);
        player = createEntity(center.x, center.y+125, 'player', playerData)
        enemy = createEntity(center.x, center.y-125, enemyData.name, enemyData)
    },
    BATTLE_ENEMY_ATTACK({ playerData, damage }) {
        createProjectile(enemy.entity, player.entity, {
            color: [255,0,0]
        });
        k.wait(0.5, () => {
            createDamageText(player.entity, damage);
            player.hp = playerData.hp;
        })
    },
    BATTLE_PLAYER_ATTACK({ enemyData, damage }) {
        createProjectile(player.entity, enemy.entity, {});
        k.wait(0.5, () => {
            createDamageText(enemy.entity, damage);
            enemy.hp = enemyData.hp;
        })
    },
    BATTLE_WIN({ playerData }) {
        updateInfo(playerData)
        enemy.die();
    },
    BATTLE_DIE() {
        player.die();
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

        if(player && 'playerData' in actionArgs) {
            updateInfo(actionArgs['playerData']);
            player.mp = actionArgs['playerData'].mp;
            if(actionName == 'MESSAGE') {
                player.hp = actionArgs['playerData'].hp;
            }
        }

        if(enemy && 'enemyData' in actionArgs) {
            enemy.mp = actionArgs['enemyData'].mp;
        }

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