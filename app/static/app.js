const { createApp } = Vue
const colorDamage = '#d32f2f'
const colorHeal = '#49F7B4'
const colorEnergy = '#b319d2'
const colorExperience = '#0DCAF0'
const colorMiss = '#ffff'

function deepMerge(target, patch) {
    if (target === null || typeof target !== 'object') {
        return structuredClone(patch);
    }

    for (const key in patch) {
        const patchVal = patch[key];
        const targetVal = target[key];

        if (Array.isArray(patchVal)) {
            target[key] = [...patchVal];
        } else if (
            patchVal !== null &&
            typeof patchVal === 'object'
        ) {
            target[key] = deepMerge(targetVal, patchVal);
        } else {
            target[key] = patchVal;
        }
    }

    return target;
}

const app = createApp({
    data() {
        return {
            erroMultiplosClientes: false,
            autenticado: false,
            podeEnviarAcao: true,
            jogador: null,
            inimigo: null,
            masmorra: null,
            tamanhoInventario: 8,
            inventario: [],
            usarAutomaticoVidaNome: null,
            usarAutomaticoEnergiaNome: null,
            atributosEquipamentosJogador: null,
            messages: [],
            conexoes: {},
            missoes: [],
            nome: '',
            email: '',
            senha: '',
            audioLigado: false,
            confirmarSenha: '',
            cadastrando: false,
            conexaoAtual: null,
            placar_de_lideres: []
        }
    },
    mounted() {
        document.body.classList.remove('opacity-0');
        this.wsConnect();
    },
    computed: {
        jogadorEstadoClasses() {
            return this.jogador ? this.jogador.estados.map(e => (e.nome.toLowerCase())) : [];
        },
        inimigoEstadoClasses() {
            return this.inimigo ? this.inimigo.estados.map(e => (e.nome.toLowerCase())) : [];
        },
        jogadorProximaMissao(){
            if(!this.jogador) return;
            const chaves = Object.keys(this.missoes);
            for(missao_chave in this.missoes) {
                const missao = this.missoes[missao_chave];
                if(!missao['completa']) return missao;
            }
            return null;
        }
    },
    watch: {
        audioLigado() {
            document.querySelectorAll('audio').forEach(el => {
                el.volume = this.audioLigado ? 1 : 0
            });
        }
    },
    methods: {
        wsConnect() {
            const ws = new WebSocket(window.WS_URL)
            const conexaoId = Date.now().toString()
            
            ws.onopen = () => {
                this.conexoes[conexaoId] = ws
                this.conexaoAtual = conexaoId
                console.log(`Conexão ${conexaoId} estabelecida`)
            }
            
            ws.onmessage = (event) => {
                this.wsReceive(event)
            }
            
            ws.onclose = () => {
                console.log(`Conexão ${conexaoId} fechada`)
                delete this.conexoes[conexaoId]
                if (this.conexaoAtual === conexaoId) {
                    this.conexaoAtual = Object.keys(this.conexoes)[0] || null
                }
            }

            ws.onerror = (error) => {
                console.error(`Erro na conexão ${conexaoId}:`, error)
                this.erroMultiplosClientes = true;
            }
        },
        wsSend(type, data) {
            const ws = this.conexoes[this.conexaoAtual]
            if (ws && ws.readyState === WebSocket.OPEN) {
                ws.send(JSON.stringify({
                    type: type,
                    data: data
                }))
                this.podeEnviarAcao = false
            }
        },
        wsReceive(event) {
            const data = JSON.parse(event.data)
            if(data.type == 'update') {
                this.wsAnimate(data);
            }
            if (data.type === 'update' || data.type === 'paused' || data.type == 'action_response') {
                this.wsUpdateState(data);
            }
            if(data.type == 'error') {
                this.criarToast('Erro', data.message)
            }
            this.usarAutomatico();
        },
        wsAnimate(data) {
            if(this.jogador && data.jogador) {
                this.wsAnimateJogador(data);
            }
            if(this.inimigo && data.inimigo && this.inimigo.id_unico == data.inimigo.id_unico) {
                this.wsAnimateInimigo(data);
            }
        },
        wsAnimateJogador(data) {
                const diferencaVida = data.jogador.vida - this.jogador.vida;
                if(diferencaVida > 0) {
                    this.criarTextoFlutuante(diferencaVida, 'jogador', colorHeal);
                } else if(diferencaVida < 0) {
                    this.criarParticulas({
                        'alvo': 'jogador',
                        'sprite_arquivo': data.inimigo.sprite_particula
                    }).then((top, left) => {
                        this.tocarAudio('#audio_dano_jogador');
                        this.criarTextoFlutuante(diferencaVida, 'jogador', colorDamage, 32, top, left);
                    });
                } else {
                    if(this.masmorra.nome != 'Casa') {
                        this.criarTextoFlutuante('0', 'jogador', colorMiss, 24);
                    }
                }

            const diferencaEnergia = data.jogador.energia - this.jogador.energia;
            if(diferencaEnergia > 0) {
                this.criarTextoFlutuante(diferencaEnergia, 'jogador', colorEnergy);
                // this.tocarAudio('#audio_exp_up');
            } else if(diferencaEnergia < 0) {
                this.criarTextoFlutuante(diferencaEnergia, 'jogador', colorEnergy);
            }

            const diferencaExperiencia = data.jogador.experiencia - this.jogador.experiencia;
            if(diferencaExperiencia > 0) {
                this.criarParticulas({
                    'alvo': 'jogador',
                    'sprite_arquivo': 'particulas/experiencia.webp',
                    'opacidade': .5
                }).then((top, left) => {
                    this.tocarAudio('#audio_exp_up');
                    this.criarTextoFlutuante(diferencaExperiencia, 'jogador', colorExperience, 32, top, left);
                });
            }

            if(data.jogador.classe.nivel > this.jogador.classe.nivel) {
                this.criarTextoFlutuante(`Classe UP!`, 'jogador', colorExperience, 18);
            }

            if(data.jogador.level > this.jogador.level) {
                this.criarParticulas({
                    'alvo': 'jogador',
                    'sprite_arquivo': 'particulas/level.webp',
                    'aleatorio': false,
                    'tamanho': 2,
                    'opacidade': .5
                }).then((top, left)=> {
                    this.tocarAudio('#audio_level_up');
                    this.criarTextoFlutuante(`Level UP!`, 'jogador', colorExperience, 18, top, left);
                });
            }
        },
        wsAnimateInimigo(data) {
            const diferencaVida = data.inimigo.vida - this.inimigo.vida;
            if(diferencaVida > 0) {
                this.criarTextoFlutuante(diferencaVida, 'inimigo', colorHeal);
            } else if(diferencaVida < 0) {
                this.criarParticulas({
                    'alvo': 'inimigo',
                    'sprite_arquivo': 'particulas/ataque_basico.webp'
                }).then((top, left) => {
                    this.tocarAudio('#audio_dano_monstro');
                    this.criarTextoFlutuante(diferencaVida, 'inimigo', colorDamage, 32, top, left);
                });
            } else {
                if(this.masmorra.nome != 'Casa') {
                    this.criarTextoFlutuante('0', 'inimigo', colorMiss, 24);
                }
            }
        },
        wsUpdateState(data) {
            this.podeEnviarAcao = true;
            if(data.jogador) {
                if(!this.autenticado) {
                    this.autenticado = true;
                    document.querySelector('#audio_musica').play();
                    setTimeout(() => {
                        const tooltipTriggerList = document.querySelectorAll('[data-bs-toggle="tooltip"]')
                        const tooltipList = [...tooltipTriggerList].map(tooltipTriggerEl => new bootstrap.Tooltip(tooltipTriggerEl))
                    }, 250)
                }
            }
            if(data.placar_de_lideres) {
                this.placar_de_lideres = data.placar_de_lideres;
            }
            if(data.jogador){
                this.jogador = deepMerge(this.jogador, data.jogador);
            }
            if(data.inventario){
                this.inventario = data.inventario
                // this.inventario = deepMerge(this.inventario, data.inventario);
            }
            if(data.inimigo) {
                this.inimigo = deepMerge(this.inimigo, data.inimigo);
            }
            if(data.masmorra) {
                this.masmorra = deepMerge(this.masmorra, data.masmorra);
            }
            if(data.masmorras) {
                this.masmorras = deepMerge(this.masmorras, data.masmorras);
            }
            if(data.atributos_equipamentos_jogador) {
                this.atributosEquipamentosJogador = data.atributos_equipamentos_jogador;
            }
            if(data.tamanho_inventario) {
                this.tamanhoInventario = data.tamanho_inventario;
            }
            if(data.missoes) {
                this.missoes = data.missoes;
            }
        },
        usarAutomatico() {
            if(!this.jogador) return;
            if(this.usarAutomaticoVidaNome) {
                const precisaUsar = this.jogador.vida + this.usarAutomaticoVidaFator <= this.jogador.vida_maxima || this.jogador.vida <= this.jogador.vida_maxima * 0.25;
                if(precisaUsar) {
                    const itemIndice = this.inventario.findIndex(item => item.nome == this.usarAutomaticoVidaNome);
                    if(itemIndice < 0) {
                        this.usarAutomaticoVidaNome = null;
                        this.usarAutomaticoVidaFator = null;
                    }
                    else {
                        this.itemAcao(itemIndice, 'usar');
                    }
                }
            } 
            if(this.usarAutomaticoEnergiaNome && this.jogador.energia + this.usarAutomaticoEnergiaFator <= this.jogador.energia_maxima) {
                const precisaUsar = this.jogador.energia + this.usarAutomaticoEnergiaFator <= this.jogador.energia_maxima || this.jogador.energia <= this.jogador.energia_maxima * 0.25;
                if(precisaUsar) {
                    const itemIndice = this.inventario.findIndex(item => item.nome == this.usarAutomaticoEnergiaNome);
                    if(itemIndice < 0) {
                        this.usarAutomaticoEnergiaNome = null;
                        this.usarAutomaticoEnergiaFator = null;
                    }
                    else {
                        this.itemAcao(itemIndice, 'usar');
                        console.log(itemIndice);
                    }
                }
            } 
        },
        processarDescricaoItem(descricao) {
            return descricao.map((linha) => {
                _linha = linha.replace('ATTR_FORCA', '<span class="material-symbols-outlined">fitness_center</span>')
                _linha = _linha.replace('ATTR_AGILIDADE', '<span class="material-symbols-outlined">directions_run</span>')
                _linha = _linha.replace('ATTR_RESISTENCIA', '<span class="material-symbols-outlined">shield</span>')
                _linha = _linha.replace('ATTR_INTELIGENCIA', '<span class="material-symbols-outlined">psychology</span>')
                _linha = _linha.replace('ATTR_VIDA', '<span class="font-bold" style="color:#198754">Pontos de Vida</span>')
                _linha = _linha.replace('ATTR_ENERGIA', '<span class="font-bold" style="color:#1976d2">Pontos de Energia</span>')
                return `<span class="d-flex align-items-center gap-1 w-full mb-1">${_linha}</span>`;
            }, '').join('');
        },
        toggleCadastrando() {
            this.cadastrando = !this.cadastrando;
        },
        tocarAudio(id) {
            setTimeout(() => {
                const audio = document.querySelector(id);
                audio.pause();
                audio.currentTime = 0;
                audio.play();
            }, Math.random()*250)
        },
        itemAcao(indice, acao) {
            if(acao == 'usar_automatico') {
                const item = this.inventario[indice]
                if(item.atributo == 'vida') {
                    if(this.usarAutomaticoVidaNome == item.nome) this.usarAutomaticoVidaNome = null;
                    else {
                        this.usarAutomaticoVidaNome = item.nome;
                        this.usarAutomaticoVidaFator = item.fator;
                    }
                } else if(item.atributo == 'energia') {
                    if(this.usarAutomaticoEnergiaNome == item.nome) this.usarAutomaticoEnergiaNome = null;
                    else {
                        this.usarAutomaticoEnergiaNome = item.nome;
                        this.usarAutomaticoEnergiaFator = item.fator;
                    }
                }
            } if(acao == 'usar') {
                this.wsSend('usar_item', { item_indice: indice });
            } else if(acao == 'descartar') {
                this.wsSend('descartar_item', { item_indice: indice });
            } else if(acao == 'descartar_todos') {
                this.wsSend('descartar_item_todos', { item_indice: indice });
            }
        },
        criarToast(titulo, conteudo) {
            const toast = document.createElement('div');
            toast.classList.add('toast', 'fade', 'show');

            const header = document.createElement('div');
            header.classList.add('toast-header');
            
            const title = document.createElement('strong');
            title.innerHTML = titulo;

            const closeButton = document.createElement('button');
            closeButton.classList.add('ms-auto', 'btn');
            closeButton.setAttribute('data-bs-dismiss', 'toast');
            closeButton.innerHTML = '✖'

            const body = document.createElement('div');
            body.classList.add('toast-body');
            body.innerHTML = conteudo;

            header.appendChild(title);
            header.appendChild(closeButton);
            toast.appendChild(header);
            toast.appendChild(body);
            document.querySelector('#toast-container').appendChild(toast);
        },
        criarTextoFlutuante(texto, alvo, cor, tamanho=32, top=null, left=null) {
            return new Promise((resolve) => {
                const container = document.querySelector(`.${alvo}-card .sprite-container`);
                const textoFlutuante = document.createElement('div');

                textoFlutuante.className = 'texto-flutuante';
                textoFlutuante.style.color = cor;
                textoFlutuante.style.fontSize = tamanho + 'px';
                textoFlutuante.textContent = texto;
                if(top == null) top = 50;
                else top -= 16;
                if(left == null) left = Math.random() * 75;
                
                textoFlutuante.style.top = `${top}%`;
                textoFlutuante.style.left = `${left}%`;
                container.appendChild(textoFlutuante);

                setTimeout(() => {
                    textoFlutuante.remove();
                    resolve();
                }, 1000);
            });
        },
        criarParticulas({alvo, sprite_arquivo, aleatorio=true, tamanho=1, duracao=750, opacidade=1}) {
            return new Promise((resolve) => {
                const container = document.querySelector(`.${alvo}-card .sprite-container`);
                const elementParticula = document.createElement('div');
                const top = aleatorio ? 12.5 + Math.random() * 50 : 50
                const left = aleatorio ? 12.5 + Math.random() * 50 : 50
                elementParticula.style.top = `${top}%`;
                elementParticula.style.left = `${left}%`;
                elementParticula.classList.add('particula-dano');
                elementParticula.style.animationDuration = `${duracao}ms`;
                elementParticula.style.opacity = opacidade;
                if(tamanho != 1) {
                    elementParticula.style.transform = `translate(-50%, -50%) scale(${tamanho})`;
                }
                elementParticula.style.setProperty('--particula-sprite', `url('static/${sprite_arquivo}')`)
                container.appendChild(elementParticula);

                setTimeout(() => {
                    elementParticula.remove();
                }, duracao-50);

                setTimeout(() => {
                    resolve(top, left);
                }, duracao/15);
            })
        },
        login() {
            if(this.cadastrando) {
                this.wsSend('signup', { nome: this.nome, email: this.email, senha: this.senha, confirmar_senha: this. confirmarSenha});
            } else {
                this.wsSend('login', { email: this.email, senha: this.senha });
            }
        },
        toggleSons() {
            this.audioLigado = !this.audioLigado;
        },
        mudarMasmorra(masmorraChave) {
            this.wsSend('mudar_masmorra', { masmorra: masmorraChave });
        },
        aumentarAtributo(atributo) {
            this.wsSend('aumentar_atributo', { atributo: atributo });
        },
        enviarAcao(acao) {
            this.wsSend('acao_jogador', { acao: acao });
        },
        subirNivelClasse(classe) {
            this.wsSend('subir_nivel_classe', { classe: classe });
        }
    }
})

app.config.compilerOptions.delimiters = ['[[', ']]'];

app.mount('#app')