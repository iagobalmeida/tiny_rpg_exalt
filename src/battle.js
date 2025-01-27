import { randomEncounter, regions } from './regions';

const playerData = localStorage.getItem('playerData') ? JSON.parse(localStorage.getItem('playerData')) : {
    level: 1,
    exp: 0,
    hp: 100,
    maxHP: 100,
    gold: 10,
    dex: 10,
    att: 10,
    def: 2
}

const playerAddExperience = (ammount) => {
    playerData.exp += ammount;
    if(playerData.exp >= playerData.level*75) {
        playerData.exp -= playerData.level*75;
        playerData.level++;
        playerData.att += 1;
        playerData.dex += 1;
        playerData.def += 1;
        playerData.maxHP += 15;
        playerData.hp = playerData.maxHP;
        return true;
    }
    return false;
}

const regionData = localStorage.getItem('regionData') ? JSON.parse(localStorage.getItem('regionData')) : {
    level: 1,
    maxLevel: 25,
    name: 'Beach',
    spriteName: 'beach'
}


const randomInt = (base=5) => (-1 * (Math.round(base*0.25) + Math.round(Math.random()*base*0.75)));

const calculateBattle = (player, enemyData) => {
    const ret = []
    const __enemy = {...enemyData}
    ret.push({
        action: 'battleStart',
        args: {
            playerData: {...player},
            enemyData: {...__enemy},
            regionData: {...regionData}
        }
    })

    ret.push({
        action: 'alert',
        args: {
            content: `${__enemy.name} found!`
        }
    })

    while(player.hp > 0 && __enemy.hp > 0) {
        const playerDexFactor = Math.random() * player.dex;
        const enemyDexFactor = Math.random() * __enemy.dex;
        
        if(playerDexFactor > enemyDexFactor && player.hp > 0) {
            const attackFactor = (playerDexFactor > enemyDexFactor * 2) ? 2 : 1;
            const defFactor = Math.round(Math.random() * __enemy.def)
            const playerAttack = attackFactor * randomInt(Math.max(0, player.att - defFactor));
            __enemy.hp += playerAttack;
            ret.push({
                action: 'damageEnemy',
                args: {
                    damage: playerAttack
                }
            });
        } 
        
        if(enemyDexFactor > playerDexFactor && __enemy.hp > 0) {
            const attackFactor = (enemyDexFactor > playerDexFactor * 2) ? 2 : 1;
            const defFactor = Math.round(Math.random() * player.def)
            const damageEnemy = attackFactor * randomInt(Math.max(0, __enemy.att - defFactor));
            player.hp += damageEnemy;
            ret.push({
                action: 'damagePlayer',
                args: {
                    damage: damageEnemy
                }
            });
        }
    }

    if(player.hp > 0 && __enemy.hp <= 0) {
        regionData.level = Math.min(regionData.maxLevel, regionData.level+1);
        let message = []
        if(__enemy.exp) message.push(`+${__enemy.exp} EXP`)
        if(__enemy.gold) message.push(`+${__enemy.gold} Gold`)
        ret.push({
            action: 'alert',
            args: {
                content: message.join(' ')
            }
        });
        playerData.gold += __enemy.gold;
        if(playerAddExperience(__enemy.exp)) {
            ret.push({
                action: 'alert',
                args: {
                    content: 'Level Up! +1 ATT / + 1 DEX / + 1 DEF'
                }
            });
        }

        ret.push({action: 'winPlayer', args: { playerData }});
    } else if(player.hp <= 0 && __enemy.hp > 0){ 
        ret.push({action: 'winEnemy'});
        ret.push({
            action: 'alert',
            args: {
                content: 'You died'
            }
        });
        player.hp = player.maxHP
        regionData.level = 1;
    }

    localStorage.setItem('playerData', JSON.stringify(playerData))
    localStorage.setItem('regionData', JSON.stringify(regionData))
    return ret;
}

const randomBattle = (regionName) => {
    const targetRegion = regions[regionName] || null;
    if(!targetRegion) return [{
        action: 'alert',
        args: {
            content: 'Invalid region!'
        }
    }];

    if(targetRegion.name != regionData.name) {
        regionData.level = 1;
        regionData.name = targetRegion.name;
        regionData.spriteName = targetRegion.spriteName;
        regionData.maxLevel = targetRegion.maxLevel;
    }

    const enemyData = randomEncounter(regionName, regionData.level)
    return calculateBattle(playerData, enemyData)
}

export default {
    calculateBattle,
    randomBattle
}