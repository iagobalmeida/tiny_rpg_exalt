const playerData = {
    hp: 100,
    maxHP: 100,
    dex: 10,
    att: 20
}

const enemiesData = {
    'bandit_leader': {
        name: 'bandit_leader',
        hp: 60,
        maxHP: 60,
        dex: 8,
        att: 10
    },
    'pirate': {
        name: 'pirate',
        hp: 20,
        maxHP: 20,
        dex: 16,
        att: 5
    },
    'beached_bucaneer': {
        name: 'beached_bucaneer',
        hp: 120,
        maxHP: 120,
        dex: 10,
        att: 15
    },
}

const randomInt = (base=5) => (Math.round(-1* Math.random()*base));

const calculateBattle = (player, enemy_name) => {
    const ret = []
    const __enemy = {...enemiesData[enemy_name]}
    ret.push({
        action: 'battleStart',
        args: [
            {...player},
            {...__enemy}
        ]
    })

    while(player.hp > 0 && __enemy.hp > 0) {
        const playerDexFactor = Math.random() * player.dex;
        const enemyDexFactor = Math.random() * __enemy.dex;
        
        if(playerDexFactor > enemyDexFactor) {
            const playerAttack = randomInt(player.att);
            __enemy.hp += playerAttack;
            ret.push({
                action: 'damageEnemy',
                args: [playerAttack]
            });
        } 
        
        if(enemyDexFactor > playerDexFactor || true) {
            const damageEnemy = randomInt(__enemy.att);
            player.hp += damageEnemy;
            ret.push({
                action: 'damagePlayer',
                args: [damageEnemy]
            });
        }
    }

    if(player.hp > 0 && __enemy.hp < 0) {
        ret.push({
            action: 'winPlayer', args: []
        });
    } else if(player.hp < 0 && __enemy.hp > 0){ 
        ret.push({
            action: 'winEnemy', args: []
        });
        player.hp = player.maxHP
    } else {
        ret.push({
            action: 'draw', args: []
        });
    }
    return ret;
}

const randomBattle = () => {
    const enemiesNames = Object.keys(enemiesData);
    const enemyName = enemiesNames[Math.floor(Math.random()*enemiesNames.length)];
    return calculateBattle(playerData, enemyName)
}

export default {
    calculateBattle,
    randomBattle,
    enemiesData,
    playerData
}