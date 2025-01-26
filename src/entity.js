export class Entity {
    constructor(k, positionX, positionY, spriteName, data) {
        this.positionX = positionX;
        this.positionY = positionY;
        this.data = data;
        this.entity = k.add([
            k.pos(positionX, positionY),
            k.sprite(spriteName),
            k.anchor('center'),
            k.animate(),
            k.opacity(1),
            k.rotate(),
            k.scale(),
            {
                hp: data.hp,
                maxHP: data.maxHP,
                ...data
            }
        ])
        this.lifeBarBackground = k.add([
            k.rect(72, 8),
            k.pos(positionX, positionY+48),
            k.outline(3, 'black'),
            k.color(0,0,0),
            k.anchor('center')
        ])
        this.lifeBar = this.lifeBarBackground.add([
            k.rect(Math.round(data.hp*72/data.maxHP), 8),
            k.pos(-36, -4),
            k.outline(1, 'black'),
            k.color(0,255,0)
        ])
    }

    damage(k, ammount) {
        const color = k.rgb(255, 255, 255);
        if(ammount > 0) {
            color.b = 0;
            color.r = 0;
        } else if(ammount < 0) {
            color.b = 0;
            color.g = 0;
        }
        this.entity.add([
            k.text(`${Math.abs(ammount)}`, { font: 'jersey' }),
            k.outline(2, 'black'),
            k.color(color),
            k.pos(0, -20),
            k.opacity(1),
            k.lifespan(1, { fade: 0.5 }),
            k.anchor('center'),
            k.move(k.vec2(0, -1), 60),
        ]);
        this.entity.hp += ammount;
    }

    updateLifebar() {
        const perc = Math.round(this.entity.hp*72/this.entity.maxHP)
        if(perc > this.lifeBar.width) this.lifeBar.width = Math.min(72, this.lifeBar.width+1);
        if(perc < this.lifeBar.width) this.lifeBar.width = Math.max(0, this.lifeBar.width-1);
    }
    
    die() {
        this.entity.destroy();
        this.lifeBarBackground.destroy();
    }
}

