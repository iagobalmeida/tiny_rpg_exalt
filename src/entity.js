export class Entity {
    constructor(k, positionX, positionY, name, data) {
        this.positionX = positionX;
        this.positionY = positionY;
        this.data = data;
        const spriteName = name.toLowerCase().replaceAll(' ','_');
        this.entity = k.add([
            k.pos(positionX, positionY),
            k.sprite(spriteName),
            k.anchor('center'),
            k.animate(),
            k.opacity(0),
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
            k.pos(positionX, positionY+this.entity.height/1.5),
            k.outline(3, 'black'),
            k.color(0,0,0),
            k.opacity(0),
            k.anchor('center')
        ])
        this.lifeBar = this.lifeBarBackground.add([
            k.rect(Math.round(data.hp*72/data.maxHP), 8),
            k.pos(-36, -4),
            k.outline(1, 'black'),
            k.color(0,255,0)
        ])
        k.tween(0, 1, 0.5, (v) => {this.entity.opacity = v; this.lifeBarBackground.opacity = v;})
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
            k.outline(1, 'black'),
            k.color(color),
            k.pos(0, -20),
            k.opacity(1),
            k.lifespan(1, { fade: 0.5 }),
            k.anchor('center'),
            k.move(k.vec2(0, -1), 60),
        ]);
        this.entity.hp += ammount;
        const perc = Math.ceil(this.entity.hp*72/this.entity.maxHP)
        k.tween(this.lifeBar.width, perc, .5, (v) => { this.lifeBar.width = v });
    }
    
    die(k) {
        k.tween(1, 0, 1, (v) => {this.entity.opacity = v; this.lifeBarBackground.opacity = v})
        setTimeout(() => {
            this.entity.destroy();
            this.lifeBarBackground.destroy();
        }, 1000);
    }
}

