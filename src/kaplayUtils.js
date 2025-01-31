import k from "./kaplayMain";

function progressBar(positionX, positionY, curr, max, height=8, width=72, tweenDuration=.25, color=[0,255,0], colorSteps=[]) {
    let kRectBackground = k.add([
        k.rect(width, height),
        k.pos(positionX, positionY),
        k.outline(2, 'black'),
        k.opacity(1),
        k.color(0,0,0),
        k.anchor('center')
    ]);

    let kRectForeground = kRectBackground.add([
        k.rect(Math.round(width*curr/max), height),
        k.pos(-36, -height/2),
        k.outline(2, 'black'),
        k.color(color[0], color[1], color[2]),
        {
            maxWidth: width,
            foregroundWidth: Math.round(width*curr/max),
            curr: curr,
            max: max
        }
    ]);

    colorSteps = colorSteps.sort((a,b) =>(b.porc - a.porc))
    let update = (value) => {
        let porc = value/kRectForeground.max
        kRectForeground.foregroundWidth = Math.round(kRectForeground.maxWidth*porc);
        if(colorSteps) {
            colorSteps.forEach(v => {
                let __porc = kRectForeground.width/kRectForeground.maxWidth
                if(__porc <= v.porc) {
                    kRectForeground.color.r = v.color[0]
                    kRectForeground.color.g = v.color[1]
                    kRectForeground.color.b = v.color[2]
                }
            });
        }
    }
    let destroy = () => {
        k.tween(1, 0, tweenDuration, (o) => { kRectBackground.opacity = o });
        k.wait(tweenDuration, () => {
            kRectBackground.destroy();
            kRectForeground.destroy();
        })
    }
    k.loop(tweenDuration, () => {
        k.tween(kRectForeground.width, kRectForeground.foregroundWidth, tweenDuration, (v) => { kRectForeground.width = v });
    })
    return {
        kRectBackground,
        kRectForeground,
        update,
        destroy
    }
}

export function damageText(entity, ammount, lifeSpan=1) {
    let color = '#ffffff';
    if(ammount > 0) color = '#00ff00';
    if(ammount < 0) color = '#ff0000';
    entity.add([
        k.text(`${Math.abs(ammount)}`, { font: 'jersey' }),
        k.color(color),
        k.pos(0, -20),
        k.opacity(1),
        k.lifespan(lifeSpan, { fade: 0.5 }),
        k.anchor('center'),
        k.z(99),
        k.move(k.vec2(0, -1), 60),
    ]);
}

export function attackProjectile(entity, target, color=[255,255,255], speed=300, offset=5) {
    const positionX = (-1 * offset) + (Math.random()*offset*2)
    entity.add([
        k.rect(8,32),
        k.anchor('center'),
        k.color(color),
        // k.outline(2, k.rgb(0,0,0)),
        k.pos(positionX, 0),
        k.opacity(1),
        k.lifespan(.55),
        k.z(99),
        k.move(target.pos.angle(entity.pos), speed)
    ]);
}

export const createMessage = (text, duration=1, infinite=false) => {
    const center = k.center();
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

export const createBackground = (spriteName=null) => {
    if(spriteName == null) {
        k.add([
            k.rect(480,480),
            k.color(k.rgb(0,0,0))
        ])
        createMessage('Start Exploring', 1, true);
    } else {
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
}



export const createRegionInfo = ({ name, level, maxLevel }) => {
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


export class Entity {
    constructor(positionX, positionY, name, data) {
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
                ...data
            }
        ])
        const barPositionY = positionY + this.entity.height/1.5;
        this.lifeBar = progressBar(positionX, barPositionY, data.hp, data.maxHP, 10, 72, .25, [0,255,0], [
            { porc:0.5, color: [255, 200, 0]},
            { porc:0.3, color: [255,0,0]}
        ]);
        this.manaBar = progressBar(positionX, barPositionY+8, data.mp, data.maxMP, 7, 72, .25, [0,0,255]);

        const direction = this.entity.pos.y > k.center().y ? 1 : -1;
        k.tween(0, 1, 0.5, (v) => {
            this.entity.opacity = v;
            this.entity.pos.y = positionY + ((1 - v) * direction * 20)
        });
    }
    
    die() {
        this.lifeBar.destroy();
        this.manaBar.destroy();
        k.tween(1, 0, 1, (v) => {
            this.entity.opacity = v;
        });
        k.wait(1, () => {
            this.entity.destroy();
        })
    }
}

