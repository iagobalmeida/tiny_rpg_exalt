const playerData = {
    hp: 100,
    maxHP: 100,
    dex: 10
}

const enemiesData = {
    'bandit_leader': {
        name: 'bandit_leader',
        hp: 60,
        maxHP: 60,
        dex: 8,
    }
}

const randomInt = () => (Math.round(-1* Math.random()*25));

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
            const playerAttack = randomInt();
            __enemy.hp += playerAttack;
            ret.push({
                action: 'damageEnemy',
                args: [playerAttack]
            });
        } 
        
        if(enemyDexFactor > playerDexFactor || true) {
            const damageEnemy = randomInt();
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
        playerData.hp = playerData.maxHP
    } else {
        ret.push({
            action: 'draw', args: []
        });
    }
    return ret;
}

const randomBattle = () => {
    return calculateBattle(playerData, 'bandit_leader')
}

export default {
    calculateBattle,
    randomBattle,
    enemiesData,
    playerData
}