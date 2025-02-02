import { randomEncounter, regions } from './regions';

const randomInt = (base=5) => (-1 * (Math.round(base*0.25) + Math.round(Math.random()*base*0.75)));

const CommunicationActions = Object.freeze({
    BATTLE_START: "BATTLE_START",
    BATTLE_ENEMY_ATTACK: "BATTLE_ENEMY_ATTACK",
    BATTLE_PLAYER_ATTACK: "BATTLE_PLAYER_ATTACK",
    BATTLE_WIN: "BATTLE_WIN",
    BATTLE_DIE: "BATTLE_DIE",
    MESSAGE: "MESSAGE"
});

const communicationAction = (action, args={}, duration=1) => ({
    action: action,
    args: args,
    duration: duration
});

const LEVEL_UP_NEXT_FACTOR = 75;
const LEVEL_UP_ATT = 2;
const LEVEL_UP_DEX = 2;
const LEVEL_UP_DEF = 2;
const LEVEL_UP_HP = 15;
const BASE_LEVEL_HP = LEVEL_UP_HP*10;

const playerData = {
    level: 1,
    exp: 0,
    next: LEVEL_UP_NEXT_FACTOR,
    hp: BASE_LEVEL_HP,
    maxHP: BASE_LEVEL_HP,
    mp: 0,
    maxMP: 50,
    dex: 10,
    att: 10,
    def: 2
}

if(localStorage.getItem('playerData')) {
    try {
        const localStoragePlayerData = JSON.parse(localStorage.getItem('playerData'));
        Object.keys(playerData).forEach((playerDataKey) => {
            playerData[playerDataKey] = localStoragePlayerData[playerDataKey] || playerData[playerDataKey];
        });
    } catch {
        console.log('Error loading "localStorage.playerData"')
    }
}

const playerAddExperience = (ammount) => {
    playerData.exp += ammount;
    if(playerData.exp >= playerData.next) {
        playerData.exp -= playerData.next;
        playerData.level++;
        
        playerData.next = playerData.level*LEVEL_UP_NEXT_FACTOR;

        playerData.att += LEVEL_UP_ATT;
        playerData.dex += LEVEL_UP_DEX;
        playerData.def += LEVEL_UP_DEF;

        playerData.maxHP += LEVEL_UP_HP;
        playerData.hp = playerData.maxHP;
        return true;
    }
    return false;
}

const regionData = {
    level: 1,
    maxLevel: 5,
    name: 'Beach',
    spriteName: 'beach'
}

if(localStorage.getItem('regionData')) {
    try {
        const localStorageregionData = JSON.parse(localStorage.getItem('regionData'));
        Object.keys(regionData).forEach((regionDataKey) => {
            regionData[regionDataKey] = localStorageregionData[regionDataKey] || regionData[regionDataKey];
        });
    } catch {
        console.log('Error loading "localStorage.regionData"')
    }
}



const calculateBattle = (player, enemyData) => {
    const ret = []
    const __enemy = {...enemyData}
    
    ret.push(communicationAction(CommunicationActions.BATTLE_START, {
        playerData: {...player},
        enemyData: {...__enemy},
        regionData: {...regionData}
    }, .5));

    ret.push(communicationAction(CommunicationActions.MESSAGE, {
        content: `${__enemy.name} found!`
    }, .5));


    while(player.hp > 0 && __enemy.hp > 0) {
        const playerDexFactor = Math.random() * player.dex;
        const enemyDexFactor = Math.random() * __enemy.dex;
        
        if(playerDexFactor > enemyDexFactor && player.hp > 0) {
            let spellFactor = 1;
            if(player.mp >= player.maxMP) {
                ret.push(communicationAction(CommunicationActions.MESSAGE, {
                    content: 'Player used skill'
                }));
                spellFactor = 5
                player.mp = 0;
            }
            player.mp = Math.min(player.maxMP, player.mp + 5)
            __enemy.mp = Math.min(__enemy.maxMP, __enemy.mp + 2.5)

            const attackFactor = (playerDexFactor > enemyDexFactor * 2) ? 2 : 1;
            const defFactor = Math.round(Math.random() * __enemy.def)
            const playerDamage = spellFactor * attackFactor * randomInt(Math.max(0, player.att - defFactor));

            __enemy.hp += playerDamage;
            ret.push(communicationAction(CommunicationActions.BATTLE_PLAYER_ATTACK, {
                damage: playerDamage,
                playerData: {...player},
                enemyData: {...__enemy}
            }, spellFactor > 1 ? 1 : .5));
        } 
        
        if(enemyDexFactor > playerDexFactor && __enemy.hp > 0) {
            let spellFactor = 1;
            if(__enemy.mp >= __enemy.maxMP) {
                ret.push(communicationAction(CommunicationActions.MESSAGE, {
                    content: 'Enemy used skill'
                }));
                spellFactor = 5
                __enemy.mp = 0;
            }
            __enemy.mp = Math.min(__enemy.maxMP, __enemy.mp + 5)
            player.mp = Math.min(player.maxMP, player.mp + 2.5)

            const attackFactor = (enemyDexFactor > playerDexFactor * 2) ? 2 : 1;
            const defFactor = Math.round(Math.random() * player.def)
            const damageEnemy = spellFactor * attackFactor * randomInt(Math.max(0, __enemy.att - defFactor));

            player.hp += damageEnemy;
            ret.push(communicationAction(CommunicationActions.BATTLE_ENEMY_ATTACK, {
                damage: damageEnemy,
                playerData: {...player},
                enemyData: {...__enemy}
            }, spellFactor > 1 ? 1 : .5));
        }
    }

    if(player.hp > 0 && __enemy.hp <= 0) {
        regionData.level = Math.min(regionData.maxLevel, regionData.level+1);
        
        ret.push(communicationAction(CommunicationActions.BATTLE_WIN));

        let message = []
        if(__enemy.exp) message.push(`+${__enemy.exp} EXP`)
        ret.push(communicationAction(CommunicationActions.MESSAGE, {
            content: message.join(' ')
        }));

        if(playerAddExperience(__enemy.exp)) {
            ret.push(communicationAction(CommunicationActions.MESSAGE, {
                content: 'Level Up!',
                playerData: {...player}
            }));
            ret.push(communicationAction(CommunicationActions.MESSAGE, {
                content: '+1 ATT / + 1 DEX / + 1 DEF'
            }, 1.5));
        }

    } else if(player.hp <= 0 && __enemy.hp > 0){ 
        ret.push(communicationAction(CommunicationActions.BATTLE_DIE));
        ret.push(communicationAction(CommunicationActions.MESSAGE, {
            content: 'You died'
        }, 1.5));
        player.hp = player.maxHP
        regionData.level = 1;
    }

    localStorage.setItem('playerData', JSON.stringify(playerData))
    localStorage.setItem('regionData', JSON.stringify(regionData))
    return ret;
}

const randomBattle = (regionName) => {
    const targetRegion = regions[regionName] || null;
    if(!targetRegion) return [communicationAction(CommunicationActions.MESSAGE, {
        content: 'Invalid region!'
    })]

    if(targetRegion.name != regionData.name) regionData.level = 1; 

    regionData.name = targetRegion.name;
    regionData.spriteName = targetRegion.spriteName;
    regionData.maxLevel = targetRegion.maxLevel;

    const enemyData = randomEncounter(regionName, regionData.level)
    return calculateBattle(playerData, enemyData)
}

export default {
    calculateBattle,
    randomBattle
}