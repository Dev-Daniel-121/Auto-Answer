from playwright.sync_api import sync_playwright

# Credenciais
ra = '110065918'
dg = '3'
uf = 'sp'
ps = 'Bp110065#'

def run():
    with sync_playwright() as p:
        # Montando Browser
        browser = p.chromium.launch(headless=False)
        page = browser.new_page()
        page.goto("https://cmspweb.ip.tv/login")
        
        # Acesso Estudante
        acessoEstudante = page.locator('div#access-student')
        acessoEstudante.click()

        # Colocando Credenciais do Estudante
        raa = page.locator('input#ra-student')
        raa.fill(ra)
        dgg = page.locator('input#digit-student')
        dgg.fill(dg)
        uff = page.locator('select#uf-student')
        uff.select_option(value=uf)
        pss = page.locator('input#password-student')
        pss.fill(ps)

        entrar = page.locator('input#btn-login-student')
        entrar.click()

        sala = page.locator(
            ':nth-match(div#lproom_r783fda450260e0cbe-l.lproom_r783fda450260e0cbe-l.frm.w100.p10.pt, 4)'
        )
        sala.click()

        # Acesso Todas as atividades
        page.goto("https://cmsp.ip.tv/mobile/tms?auth_token=eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJza2V5IjoiYXV0aF90b2tlbjplZHVzcDpkYW5pZWxvbGl2ZTEwMDY1OTE4My1zcCIsIm5pY2siOiJkYW5pZWxvbGl2ZTEwMDY1OTE4My1zcCIsInJvbGUiOiIwMDA2IiwicmVhbG0iOiJlZHVzcCIsImlhdCI6MTczMzQ5MjQzNywiYXVkIjoid2ViY2xpZW50In0.Cb9gBJa-zktTjbfZRt3DiXq6l0u089-4Y_Bnq5JNMJg&room=r783fda450260e0cbe-l")
        todasAsAtividades = page.locator(
            ':nth-match(div.MuiBox-root.css-p0pzb2, 2)'
        )
        todasAsAtividades.click()

        """
        * Objetivo dessa função:
            TODO Fazer atividade
                TODO Armazenar conteúdo em um arquivo JSON já preparado         ✔
                
                
                ??? ========================================= ***** ========================================= ???

                *tipo_questao_1 = 'Radios'
                *tipo_questao_2 = 'Checkbox'
                *tipo_questao_3 = 'Dragable'
                *tipo_questao_4 = 'Order'
                *tipo_questao_5 = 'Textarea'
                *tipo_questao_6 = 'Select'
                
                *card_atual = 1 # Identificar o card atual e facilitar a especificação dos elementos dentro dela
                *texto_atual = 1 # Identificar o texto atual e facilitar a especificação dos elementos dentro dela
                *questao_atual = 1 # Identificar a questão atual e facilitar a especificação dos elementos dentro dela

                *card_verificado = 0 # Será para ajudar na verificação final
                *questoes_respondido = 0 # Número de questões respondidas

                # Essas variaveis vão servir para ajudar a contar e a entender quais questões aparecem mais
                *questao_texto_img_gif_video = 0
                *img_gif_video = 0
                *questao_texto = 0
                *questao_radios = 0
                *questao_checkbox = 0
                *questao_dragable = 0
                *questao_order = 0
                *questao_textarea = 0
                #! questao_select = 0
                
                *## DESCOBRIR QUANTAS VERIFICAÇÕES TEM QUE FAZER
                *numero_de_card = número de div.css-xz389d # A div.css-xz389d são cada card
                *numero_de_questao = número de div.css-nlzma4 # A div.css-nlzma4 são cada card de questões
                
                # JSON
                *atividade = {
                    contexto: 
                    '''
                        Contexto: Estou desenvolvendo um sistema de automação de processos que utiliza a IA do ChatGPT para responder perguntas. As perguntas estão em um arquivo JSON, com informações como número da pergunta, título da pergunta, tipo de pergunta, alternativas, entre outras. Enviarei esse arquivo JSON para a IA e ela deve retornar um outro arquivo JSON contendo apenas as respostas, com base nas regras que definirei a seguir.

                        Objetivo: Enviar um arquivo JSON com as informações das perguntas, e a IA deve retornar um arquivo JSON com a seguinte estrutura:

                        • Número da questão
                        • Tipo da questão
                        • Resposta da questão
                        
                        Regras para Respostas:
                            1. Radios (Alternativa única):
                                • Para questões do tipo "Radios", a IA deve retornar somente uma alternativa correta.
                                • Exemplo:
                                    atividade = {
                                        "questao_1": {
                                            "Tipo": "Radios",
                                            "Header": "Título da questão",
                                            "Alternativas": ["Alternativa A", "Alternativa B", "Alternativa C", "Alternativa D"]
                                        }
                                    }
                                    resposta = {
                                        "questao_1": {
                                            "Tipo": "Radios",
                                            "Resposta": ["Alternativa A"]
                                        }
                                    }

                            2. Checkbox (Múltiplas alternativas):
                                • Para questões do tipo "Checkbox", a IA deve retornar pelo menos uma alternativa correta, podendo ter mais de uma.
                                • Exemplo:
                                    atividade = {
                                        "questao_2": {
                                            "Tipo": "Checkbox",
                                            "Header": "Título da questão",
                                            "Alternativas": ["Alternativa A", "Alternativa B", "Alternativa C", "Alternativa D"]
                                        }
                                    }
                                    resposta = {
                                        "questao_2": {
                                            "Tipo": "Checkbox",
                                            "Resposta": ["Alternativa A", "Alternativa B", "Alternativa C"]
                                        }
                                    }

                            3. Dragable (Ordem correta dos itens):
                                • Para questões do tipo "Dragable", a IA deve retornar a ordem correta dos textos e seus respectivos índices.
                                • Exemplo:
                                    atividade = {
                                        "questao_3": {
                                            "Tipo": "Dragable",
                                            "Header": "Título da questão",
                                            "Alternativas": ["Texto_1", "Texto_2", "Texto_3", "Texto_4"]
                                        }
                                    }
                                    resposta = {
                                        "questao_3": {
                                            "Tipo": "Dragable",
                                            "Resposta": ["Texto_4", "Texto_2", "Texto_1", "Texto_3"]
                                        }
                                    }

                            4. Order (Ordem correta dos itens):
                                • Para questões do tipo "Order", a IA deve retornar a ordem correta dos textos.
                                • Exemplo:
                                    atividade = {
                                        "questao_4": {
                                            "Tipo": "Order",
                                            "Header": "Título da questão",
                                            "Alternativas": ["Palavra_1", "Palavra_2", "Palavra_3", "Palavra_4"]
                                        }
                                    }
                                    resposta = {
                                        "questao_4": {
                                            "Tipo": "Order",
                                            "Resposta": ["Palavra_2", "Palavra_1", "Palavra_3", "Palavra_4"]
                                        }
                                    }

                            5. Textarea (Resposta objetiva):
                                • Para questões do tipo "Textarea", a IA deve fornecer uma resposta breve, objetiva e de fácil compreensão, utilizando palavras com baixo grau de complexidade.
                                • Exemplo:
                                    atividade = {
                                        "questao_5": {
                                            "Tipo": "Textarea",
                                            "Header": "Título da questão"
                                        }
                                    }
                                        resposta = {
                                        "questao_5": {
                                            "Tipo": "Textarea",
                                            "Resposta": "Resposta para a pergunta"
                                        }
                                    }

                        Formato da Resposta: A resposta deve ser gerada no formato JSON, seguindo as regras definidas para cada tipo de questão.
                    '''
                }

                *respostas = {
                    resposta = {}
                }
                
                ? ### FUNÇÕES JSON ###

                *funcao salvarJSON(tipo='', head_texto='', head_questao='', alternativas_quetao='', questao_atual='', texto_atual=''):
                    se (tipo == 'Texto')
                        atividade = {
                            texto[f"texto_{texto_atual}"] = { # O $ é o valor da texto_atual
                                Tipo: tipo,
                                Texto: f'''head_texto''' # Troque ''' por aspas duplas
                            }
                        }
                    senao se (tipo == tipo_questao_1 ou tipo == tipo_questao_2 ou tipo == tipo_questao_3 ou tipo == tipo_questao_4 ou tipo == tipo_questao_5) {
                        atividade = {
                            questoes[f"questao_{questao_atual}"] = { # O $ é o valor da questao_atual
                                Tipo: tipo,
                                Header: f'''{head_questao}''',
                                Alternativas = f'''{alternativas_quetao}'''
                            }
                        }
                    }

                *funcao pegar_resposta_JSON() {
                    Pegue a resposta do arquivo JSON
                }
                
                ? ### FUNÇÕES RESPONDER ###

                *funcao responder_radios(indice_iteracao) {
                    JSON = pegar_resposta_JSON()
                    Procure dentre as div.MuiRadiosGroup-root div.css-t1yck que estão dentro do pai :nth-match('div.MuiCard-root.css-xz389d, indice_iteracao') uma que o valor seja igual ao ARQUIVO JSON # Essa especificação 'div.MuiRadiosGroup-root div.css-t1yck' é o conjunto de alternativas. Aqui a ideia é procurar dentro do card atual no conjunto de alternativas a alternativa que tem o valor igual ao do arquivo JSON com a resposta do ChatGPT
                    Click no input.PrivateSwitchBase-input.css-1m9pwf3 que está na div.MuiRadiosGroup-root div.css-t1yck que esá dentro do pai :nth-match('div.MuiCard-root.css-xz389d, indice_iteracao') cujo valor seja igual ao ARQUIVO JSON # Agora é apenas clicar no Input da alternativa
                }

                *funcao responder_checkbox(indice_iteracao) {
                    JSON = pegar_resposta_JSON()
                    Crie um array com as alternativas corretas (Idependente se for apenas 1 ou mais) # Como é do tipo checkbox é possível ter mais de uma alternativa certa
                    Itere sobre os valores e click na ordem correta # Iteraremos nesse array para por as respostas corretas
                        Procure dentre as div.MuiCheckbox-root div.css-t1yck que está dentro do pai :nth-match('div.MuiCard-root.css-xz389d, indice_iteracao') cujo valor seja igual ao ARQUIVO JSON
                        Click no input.PrivateSwitchBase-input.css-1m9pwf3 que está na div.MuiCheckbox-root div.css-t1yck que está dentro do pai :nth-match('div.MuiCard-root.css-xz389d, indice_iteracao') cujo valor seja igual ao ARQUIVO JSON
                }

                *funcao responder_dragable(indice_iteracao) {
                    JSON = pegar_resposta_JSON()
                    Crie um array para conter as alternativas na ordem correta
                    Itere sobre os valores
                        Procure dentre as div.css-z0sbrd que está dentro do pai :nth-match('div.MuiCard-root.css-xz389d, indice_iteracao') o h6.MuiTypography-root.css-rckqyx cujo o valor seja igual ao valor do indice_array_atual
                        diferenca = 0 # A diferença vai começar em 0 para cada iteração
                        diferenca = indice_array - indice da div.css-z0sbrd que está dentro do pai :nth-match('div.MuiCard-root.css-xz389d, indice_iteracao') o qual tem o h6.MuiTypography-root.css-rckqyx cujo o valor seja igual ao indice_array_atual # A diferença vai servir para saber quanto precisamos subir, descer ou ficar
                        Se (indice_array > indice da div.css-z0sbrd que está dentro do pai :nth-match('div.MuiCard-root.css-xz389d, indice_iteracao') o qual tem o h6.MuiTypography-root.css-rckqyx cujo o valor seja igual ao indice_array_atual) {
                            # Se for maior vamos descer ele
                            Click no span.MuiButtonBase-root.css-2wyiu que está dentro da div.css-z0sbrd que está dentro do pai :nth-match('div.MuiCard-root.css-xz389d, indice_iteracao') o qual tem o h6.MuiTypography-root.css-rckqyx cujo o valor seja igual ao indice_array_atual e também o svg.MuiSvgIcon-root.css-1in44b7 com o data-testid="ArrowCircleDownIcon" * diferenca # Aqui vamos fazer com que ele repita esse click a quantidade da diferença mutiplicando ele
                            Passa para próxima iteração
                        } Senão Se (indice_array < indice da div.css-z0sbrd que está dentro do pai :nth-match('div.MuiCard-root.css-xz389d, indice_iteracao') o qual tem o h6.MuiTypography-root.css-rckqyx cujo o valor seja igual ao indice_array_atual) {
                            # Se for maior vamos subir ele
                            Click no span.MuiButtonBase-root.css-2wyiu que está dentro da div.css-z0sbrd que está dentro do pai :nth-match('div.MuiCard-root.css-xz389d, indice_iteracao') o qual tem o h6.MuiTypography-root.css-rckqyx cujo o valor seja igual ao indice_array_atual e também o svg.MuiSvgIcon-root.css-1in44b7 com o data-testid="ArrowCircleUpIcon" * diferenca
                            Passa para próxima iteração
                        } Senão Se (indice_array == indice da div.css-z0sbrd que está dentro do pai :nth-match('div.MuiCard-root.css-xz389d, indice_iteracao') o qual tem o h6.MuiTypography-root.css-rckqyx cujo o valor seja igual ao indice_array_atual) {
                            Passa para próxima iteração # Se for igual apenas passe para a próxima iteração
                        }
                }

                *funcao responder_order(indice_iteracao) {
                    JSON = pegar_resposta_JSON()
                    Crie um array para armazenar os valores na ordem correta # Como é do tipo order (Ordenar) precisamos ter esse valores na ordem correta
                    Itere sobre os valores e click na ordem correta
                        Procure dentre as div.MuiButtonBase-root.css-16x8ql9 span.MuiChip-label.css-9iedg7 que está dentro do pai :nth-match('div.MuiCard-root.css-xz389d, indice_iteracao') cujo valor seja igual ao ARQUIVO JSON
                        Click no span.MuiChip-label.css-9iedg7 que está na div.MuiButtonBase-root.css-16x8ql9 que está dentro do pai :nth-match('div.MuiCard-root.css-xz389d, indice_iteracao') cujo valor seja igual ao ARQUIVO JSON
                        # Faça isso para toda a ordem
                }

                *funcao responder_textarea(indice_iteracao) {
                    JSON = pegar_resposta_JSON()
                    Click no textarea.MuiInputBase-inputMultiline.css-13pivat que está no div.MuiInput-root que está dentro do pai :nth-match('div.MuiCard-root.css-xz389d, indice_iteracao') e depois da um .fill() com o valor do JSON # Agora é apenas clicar no textarea e dar um fill (completar/encher) com a resposta do ChatGPT
                }

                ? ### FUNÇÃO VERIFICAR IMAGEM NAS ALTERNATIVAS ###

                *funcao verificar_imagens_nas_alterntativas () {
                    # Supondo que 'card_atual' é um elemento Playwright com a estrutura esperada
                    se (dentro da :nth-match('div.MuiCard-root.css-xz389d, card_atual')
                    
                    div.MuiPaper-root.css-1db9nhj > img.MuiCardMedia-root.css-5rs0y1
                }

                ? ### FUNÇÕES EXTRAIR ###
                    
                *funcao extrair_titulo_do_card(card_atual) {
                    # Supondo que 'card_atual' é um elemento Playwright com a estrutura esperada
                    head_questao = Todo o conteúdo da div com o atributo style="padding: 0px 24px;" que está dentro da div.css-1v3caum que está dentro do pai que é :nth-match('div.MuiCard-root.css-xz389d, card_atual') pegue todo e qualquer forma de Texto # Isso é para garantir que vamos pegar todo o conteúdo do título da questão
                    retorne o conteúdo do texto
                }
                
                *funcao extrair_questao_radios(card_atual) {
                    # Chama a função reutilizável para extrair o título
                    head_questao = extrair_titulo_do_card(card_atual)

                    # Procurando as alternativas (Radio Buttons)
                    alternativas_quetao = []
                    Itere sobre cada div.css-t1yck que está dentro do pai que é :nth-match('div.MuiCard-root.css-xz389d, card_atual') e guarde no array alternativas_quetao
                    SE na :nth-match(div.css-t1yck, indice_da_iteracao) EXISTI img.MuiCardMedia-root.css-5rs0y1 que está dentro da div.MuiPaper-root.css-1db9nhj {
                        Pause o programa e peça para que o usuário responda a pergunta atual e finalize a iteração aqui # Vamos finalizar a iteração para não ficar iterando em todas as outras alternativas, pois se tem 1 alternativa com uma imagem então é bom que o usuário responda pois a IA pode não conseguir responder
                    } Senão {
                        Pegue o todo e qualquer forma de Texto da div.MuiBox-root.css-kmkory que está dentro da div.css-t1yck que está dentro do pai que é :nth-match('div.MuiCard-root.css-xz389d, card_atual') # Isso é para garantir que vamos pegar todo o conteúdo da alternativa atual
                        Salve no array e passe para próxima iteração
                    }

                    retorne {
                        "titulo": head_questao,
                        "alternativas": alternativas_quetao
                    }
                }

                *funcao extrair_questao_checkbox(card_atual) {
                    # Chama a função reutilizável para extrair o título
                    head_questao = extrair_titulo_do_card(card_atual)

                    # Procurando as alternativas (Checkbox Buttons)
                    alternativas_quetao = []
                    Itere sobre cada div.css-t1yck que está dentro do pai que é :nth-match('div.MuiCard-root.css-xz389d, card_atual') e guarde no array alternativas_quetao
                    SE na :nth-match(div.css-t1yck, indice_da_iteracao) EXISTI img.MuiCardMedia-root.css-5rs0y1 que está dentro da div.MuiPaper-root.css-1db9nhj {
                        Pause o programa e peça para que o usuário responda a pergunta atual e finalize a iteração aqui # Vamos finalizar a iteração para não ficar iterando em todas as outras alternativas, pois se tem 1 alternativa com uma imagem então é bom que o usuário responda pois a IA pode não conseguir responder
                    } SENAO {
                        Pegue o todo e qualquer forma de Texto da div.MuiBox-root.css-kmkory que está dentro da div.css-t1yck que está dentro do pai que é :nth-match('div.MuiCard-root.css-xz389d, card_atual') # Isso é para garantir que vamos pegar todo o conteúdo da alternativa atual
                        Salve no array e passe para próxima iteração
                    }

                    retorne {
                        "titulo": head_questao,
                        "alternativas": alternativas_quetao
                    }
                }

                *funcao extrair_questao_dragable(card_atual) {
                    # Chama a função reutilizável para extrair o título
                    head_questao = extrair_titulo_do_card(card_atual)

                    # Procurando as alternativas (Dragable Buttons)
                    alternativas_quetao = []
                    Itere sobre cada div.css-z0sbrd que está dentro do pai que é :nth-match('div.MuiCard-root.css-xz389d, card_atual') e guarde no array alternativas_quetao
                    SE na :nth-match(div.css-t1yck, indice_da_iteracao) EXISTI img.MuiCardMedia-root.css-5rs0y1 que está dentro da div.MuiPaper-root.css-1db9nhj {
                        Pause o programa e peça para que o usuário responda a pergunta atual e finalize a iteração aqui # Vamos finalizar a iteração para não ficar iterando em todas as outras alternativas, pois se tem 1 alternativa com uma imagem então é bom que o usuário responda pois a IA pode não conseguir responder
                    } SENAO {
                        Pegue o todo e qualquer forma de Texto da div.MuiBox-root.css-16izr03 que está dentro da div.css-z0sbrd que está dentro do pai que é :nth-match('div.MuiCard-root.css-xz389d, card_atual') e também dentro de cada div.css-z0sbrd tem o data-content que dentro dele tem o "Index: número_do_index" pegue também o seu index # Isso é para garantir que vamos pegar todo o conteúdo da alternativa atual e o seu index que é a posição dela
                        Salve no array e passe para próxima iteração
                    }

                    retorne {
                        "titulo": head_questao,
                        "alternativas": alternativas_quetao
                    }
                }

                *funcao extrair_questao_order(card_atual) {
                    # Chama a função reutilizável para extrair o título
                    head_questao = extrair_titulo_do_card(card_atual)

                    # Procurando as alternativas (Order Buttons)
                    alternativas_quetao = []
                    Itere sobre cada div.MuiChip-root.css-16x8ql9 que está dentro do pai que é :nth-match('div.MuiCard-root.css-xz389d, card_atual') e guarde no array alternativas_quetao
                    SE na :nth-match(div.css-t1yck, indice_da_iteracao) EXISTI img.MuiCardMedia-root.css-5rs0y1 que está dentro da div.MuiPaper-root.css-1db9nhj {
                        Pause o programa e peça para que o usuário responda a pergunta atual e finalize a iteração aqui # Vamos finalizar a iteração para não ficar iterando em todas as outras alternativas, pois se tem 1 alternativa com uma imagem então é bom que o usuário responda pois a IA pode não conseguir responder
                    } SENAO {
                        Pegue o todo e qualquer forma de Texto do span.MuiChip-label.css-9iedg7 que está dentro da div.MuiChip-root.css-16x8ql9 que está dentro do pai que é :nth-match('div.MuiCard-root.css-xz389d, card_atual') # Isso é para garantir que vamos pegar todo o conteúdo da alternativa atual
                        Salve no array e passe para próxima iteração
                    }

                    retorne {
                        "titulo": head_questao,
                        "alternativas": alternativas_quetao
                    }
                }

                *funcao extrair_questao_textarea(card_atual) {
                    # Chama a função reutilizável para extrair o título
                    head_questao = extrair_titulo_do_card(card_atual)

                    retorne {
                        "titulo": head_questao,
                    }
                }

                !funcao extrair_questao_select(card_atual) {}

                *FACA { # Vamos fazer tudo isso enquanto o número de numero_de_card for maior que o card_verificado ou seja ainda faltam cards para verificar
                    # Aqui vamos zerar as variaveis
                    head_texto = ''
                    head_questao = ''
                    tipo_questao = ''
                    alternativas_quetao = []
                    
                    *SE (dentro da :nth-match('div.css-xz389d, card_atual') EXISTI a div.css-1mi3tt8 OU EXISTI a div.ytp-cued-thumbnail-overlay OU EXISTI a img com o atributo style="max-width: 100%;" { # Esse card_verificado ajuda a saber qual é o card atual ou o card que estamos verificando
                        # Se existir então temos aqui um PDF ou VÍDEO ou GIF Agora vamos verificar se tem alguma conteúdo que possa ser importante nós pegar
                        *SE (dentro da :nth-match('div.css-xz389d, card_atual') EXISTI h6.MuiTypography-root.MuiTypography-subtitle2.css-qpwa0j) {
                            # Se tiver um deles vamos verificar se EXISTI h6.MuiTypography-root.MuiTypography-subtitle2.css-qpwa0j o que significa que temos um breve texto sobre o assunto
                            head_texto = Todo o conteúdo do :nth-match('h6.MuiTypography-root.MuiTypography-subtitle2.css-qpwa0j, texto_atual') pegue todo e qualquer forma de Texto
                            tipo = 'Texto'

                            # Armazene todo esse conteúdo no dicionário para depois passar para o JSON
                            salvarJSON(tipo, texto_atual, head_texto)
                            
                            questao_texto_img_gif_video += 1
                            texto_atual += 1 # Para saber para qual texto vamos
                            card_atual += 1 # Para saber para qual card vamos
                            card_verificado += 1 # Para saber quantos cards já foram verificados
                            Passa para a próxima div.css-xz389d # Em outras palavras passar para o próximo card
                        *} SENÃO {
                            # Se não EXISTI h6.MuiTypography-root.MuiTypography-subtitle2.css-qpwa0j então provavelmente aqui tem só um PDF ou VÍDEO ou GIF
                            img_gif_video += 1
                            card_atual += 1
                            card_verificado += 1 # Para saber quantos cards já foram verificados
                            Passa para a próxima div.css-xz389d
                        }
                    *} SENÃO {
                        *SE (dentro da :nth-match('div.css-xz389d, card_atual') EXISTI h6.MuiTypography-root.MuiTypography-subtitle2.css-qpwa0j) {
                            # Se não tiver nenhum PDF, VÍDEO ou GIF vamos verificar se é um card só de texto
                            head_questao = extrair_texto_do_card(card_atual)
                            tipo = 'Texto'

                            # Armazene todo esse conteúdo no dicionário para depois passar para o JSON
                            salvarJSON(tipo, texto_atual, head_texto)

                            texto_atual += 1
                            card_atual += 1
                            questao_texto += 1
                            card_verificado += 1
                            Passa para a próxima div.css-xz389d
                        *} SENÃO {
                            # Se não é um card que contem TEXTO, PDF, VÍDEO ou GIF então só pode ser uma questão
                            *SE (dentro da :nth-match('div.css-xz389d, card_atual') EXISTI div.css-nlzma4) {
                                # Se tiver essa div então sabemos que é uma questão então agora verificamos o tipo de questão (Radios, Checkbox, etc)
                                # Sistema/Função para identificar tipo de pergunta
                                *SE (dentro da :nth-match('div.MuiCard-root.css-xz389d, card_atual') EXISTI span.MuiRadios-root.css-1sgsc5r) {
                                    # Se existir então é uma questão de tipo Radios
                                    card_verificado += 1
                                    
                                    # Armazene todo esse conteúdo no dicionário para depois passar para o JSON
                                    questao_radios = extrair_questao_radios(card_atual)

                                    # Armazene todo esse conteúdo no dicionário para depois passar para o JSON
                                    salvar_json(tipo_questao_1, questao_atual, questao_radio['titulo'], questao_radio['alternativas'])

                                    questoes_respondido += 1 # Vamos adicionar mais 1 ao número de questões respondidas
                                    questao_atual += 1
                                    questao_radios += 1
                                    Para e passa para a próxima pergunta
                                *} SENÃO SE (dentro da :nth-match('div.MuiCard-root.css-xz389d, card_atual') EXISTI span.MuiCheckbox-root.css-14bgux8) {
                                    # Se existir então é uma questão de tipo Checkbox
                                    card_verificado += 1
                                    
                                    # Armazene todo esse conteúdo no dicionário para depois passar para o JSON
                                    questao_checkbox = extrair_questao_checkbox(card_atual)

                                    # Armazene todo esse conteúdo no dicionário para depois passar para o JSON
                                    salvar_json(tipo_questao_2, questao_atual, questao_checkbox['titulo'], questao_checkbox['alternativas'])
                                
                                    questoes_respondido += 1
                                    questao_atual += 1
                                    questao_checkbox += 1
                                    Para e passa para a próxima pergunta
                                *} SENÃO SE (dentro da :nth-match('div.MuiCard-root.css-xz389d, card_atual') EXISTI span.MuiCheckbox-root.css-14bgux8) {
                                    # Se existir então é uma questão de tipo Dragable
                                    card_verificado += 1
                                    
                                    # Armazene todo esse conteúdo no dicionário para depois passar para o JSON
                                    questao_dragable = extrair_questao_dragable(card_atual)

                                    # Armazene todo esse conteúdo no dicionário para depois passar para o JSON
                                    salvar_json(tipo_questao_3, questao_atual, questao_dragable['titulo'], questao_dragable['alternativas'])
                                    
                                    questoes_respondido += 1
                                    questao_atual += 1
                                    questao_dragable += 1
                                    Para e passa para a próxima pergunta
                                *} SENÃO SE (dentro da :nth-match('div.MuiCard-root.css-xz389d, card_atual') EXISTI div.MuiChip-Default.css-16x8ql9) {
                                    # Se existir então é uma questão de tipo Order
                                    card_verificado += 1
                                    
                                    # Armazene todo esse conteúdo no dicionário para depois passar para o JSON
                                    questao_order = extrair_questao_order(card_atual)

                                    # Armazene todo esse conteúdo no dicionário para depois passar para o JSON
                                    salvar_json(tipo_questao_4, questao_atual, questao_order['titulo'], questao_order['alternativas'])

                                    questoes_respondido += 1
                                    questao_atual += 1
                                    questao_order += 1
                                    Para e passa para a próxima pergunta
                                *} SENÃO SE (dentro da :nth-match('div.MuiCard-root.css-xz389d, card_atual') EXISTI div.MuiTextField-root.css-feqhe6) {
                                    # Se existir então é uma questão de tipo Textarea
                                    card_verificado += 1
                                    
                                    # Armazene todo esse conteúdo no dicionário para depois passar para o JSON
                                    questao_textarea = extrair_questao_textarea(card_atual)

                                    # Armazene todo esse conteúdo no dicionário para depois passar para o JSON
                                    salvar_json(tipo_questao_5, questao_atual, questao_textarea['titulo'])

                                    questoes_respondido += 1
                                    questao_atual += 1
                                    textarea += 1
                                    Para e passa para a próxima pergunta
                                !} SENÃO SE (dentro da :nth-match('div.MuiCard-root.css-xz389d, card_atual') EXISTI span.MuiRadios-root.css-1sgsc5r) {                                }
                            }
                        }
                            PEDIR AO USUÁRIO PARA QUERESOLVA ESSA QUESTÃO E DIGA SE JÁ RESPONDEU PARA PASSAR PARA PRÓXIMA
                        PEGA O JSON COM A PERGUNTA E AS ALTERNATIVAS DA questao_atual E PASSE PARA ChatGPT PARA QUE RESOLVA E RETORNE A RESPOSTA(s)
                        PEGA AS RESPOSTAS DESSE JSON E COLOUQE NA ALTERNATIVA CORRETA
                    }
                } ENQUANTO (numero_de_card > card_verificado)

                *Para cada div.MuiCard-root.css-xz389d div.css-1v3caum {
                    *SE (tipo_da_questao_chatgpt == tipo_questao_atual) {
                        # Valida se o tipo da questão que o ChatGPT fez é o mesmo da original
                        *SE (tipo_da_questao_chatgpt == tipo_questao_1) {
                            # Valida o tipo da questão
                            *SE (número_de_respostas == 1) {
                                # Valida a resposta e responde
                                responder_radios(indice_iteracao)
                            } SENAO {
                                Solicite ao usuário para que verifique a questão_NÚMERO_DA_QUESTÃO e espere até precione "Enter" na solicitação
                                Passe para próxima div.css-1v3caum
                            }
                        *} SENAO SE (tipo_da_questao_chatgpt == tipo_questao_2) {
                            # Valida o tipo da questão
                            *SE (número_de_respostas >= 1) {
                                # Valida a resposta e responde
                                responder_checkbox(indice_iteracao)
                            } SENAO {
                                Solicite ao usuário para que verifique a questão_NÚMERO_DA_QUESTÃO e espere até precione "Enter" na solicitação
                                Passe para próxima div.css-1v3caum
                            }
                        *} SENAO SE (tipo_da_questao_chatgpt == tipo_questao_3) {
                            # Valida o tipo da questão
                            *SE (número_de_respostas >= 1) {
                                # Valida a resposta e responde
                                responder_dragable(indice_iteracao)
                            } SENAO {
                                Solicite ao usuário para que verifique a questão_NÚMERO_DA_QUESTÃO e espere até precione "Enter" na solicitação
                                Passe para próxima div.css-1v3caum
                            }
                        *} SENAO SE (tipo_da_questao_chatgpt == tipo_questao_4) {
                            # Valida o tipo da questão
                            *SE (número_de_respostas >= 1) {
                                # Valida a resposta e responde
                                responder_order(indice_iteracao)
                            } SENAO {
                                Solicite ao usuário para que verifique a questão_NÚMERO_DA_QUESTÃO e espere até precione "Enter" na solicitação
                                Passe para próxima div.css-1v3caum
                            }
                        *} SENAO SE (tipo_da_questao_chatgpt == tipo_questao_5) {
                            # Valida o tipo da questão
                            SE (número_de_respostas >= 1) {
                                # Valida a resposta e responde
                                responder_textarea(indice_iteracao)
                            } SENAO {
                                Solicite ao usuário para que verifique a questão_NÚMERO_DA_QUESTÃO e espere até precione "Enter" na solicitação
                                Passe para próxima div.css-1v3caum
                            }
                        }
                    *} SENAO {
                        Solicite ao usuário para que verifique a questão_NÚMERO_DA_QUESTÃO e espere até precione "Enter" na solicitação
                        Passe para próxima div.css-1v3caum
                    }
                }
                
                ? ====================================== Radio ====================================== ?
                
                    ? # Sistema/Função para procurar respostas
                    ?    Abra uma nova guia
                    ?    Entre em https://chatgpt.com/)
                    ?    Pega todo o conteúdo do JSON e coloca no ChatGPT
                    ?    resposta_GPT = Pege a reposta do ChtGPT
                    ?    respostas = { # Salvar no arquivo JSON para resposta
                    ?        resposta_GPT
                    ?    }

                    * # Sistema/Função para responder respostas do tipo Radios
                    *    Pegue a resposta do arquivo JSON
                    *    Procure dentre as div.MuiRadiosGroup-root div.css-t1yck que estão dentro do pai :nth-match('div.MuiCard-root.css-xz389d, card_atual') uma que o valor seja igual ao ARQUIVO JSON # Essa especificação 'div.MuiRadiosGroup-root div.css-t1yck' é o conjunto de alternativas. Aqui a ideia é procurar dentro do card atual no conjunto de alternativas a alternativa que tem o valor igual ao do arquivo JSON com a resposta do ChatGPT
                    *    Click no input.PrivateSwitchBase-input.css-1m9pwf3 que está na div.MuiRadiosGroup-root div.css-t1yck que esá dentro do pai :nth-match('div.MuiCard-root.css-xz389d, card_atual') cujo valor seja igual ao ARQUIVO JSON # Agora é apenas clicar no Input da alternativa

                ? ====================================== Checkbox ====================================== ?

                    ? # Sistema/Função para procurar respostas
                    ?    Vá para a página do ChatGPT (Abra uma nova guia, Entre em https://chatgpt.com/)
                    ?    Pega todo o conteúdo do JSON e coloca no ChatGPT
                    ?    Pega a resposta do ChatGPT que vai vim em formato JSON e armazene em outro arquivo JSON
                    
                    * # Sistema/Função para responder respostas do tipo Radios
                    *    Pegue a resposta do arquivo JSON
                    *    Crie um array com as alternativas corretas (Idependente se for apenas 1 ou mais) # Como é do tipo checkbox é possível ter mais de uma alternativa certa
                    *    Itere sobre os valores e click na ordem correta # Iteraremos nesse array para por as respostas corretas
                    *        Procure dentre as div.MuiCheckbox-root div.css-t1yck que está dentro do pai :nth-match('div.MuiCard-root.css-xz389d, card_atual') cujo valor seja igual ao ARQUIVO JSON
                    *        Click no input.PrivateSwitchBase-input.css-1m9pwf3 que está na div.MuiCheckbox-root div.css-t1yck que está dentro do pai :nth-match('div.MuiCard-root.css-xz389d, card_atual') cujo valor seja igual ao ARQUIVO JSON

                ? ====================================== Dragable ====================================== ?

                    * # Sistema/Função para responder respostas do tipo Dragable
                    *    Pegue a resposta do arquivo JSON
                    *    Crie um array para conter as alternativas na ordem correta
                    *    Itere sobre os valores
                    *        Procure dentre as div.css-z0sbrd que está dentro do pai :nth-match('div.MuiCard-root.css-xz389d, card_atual') o h6.MuiTypography-root.css-rckqyx cujo o valor seja igual ao valor do indice_array_atual
                    *        diferenca = 0 # A diferença vai começar em 0 para cada iteração
                    *        diferenca = indice_array - indice da div.css-z0sbrd que está dentro do pai :nth-match('div.MuiCard-root.css-xz389d, card_atual') o qual tem o h6.MuiTypography-root.css-rckqyx cujo o valor seja igual ao indice_array_atual # A diferença vai servir para saber quanto precisamos subir, descer ou ficar
                    *        Se (indice_array > indice da div.css-z0sbrd que está dentro do pai :nth-match('div.MuiCard-root.css-xz389d, card_atual') o qual tem o h6.MuiTypography-root.css-rckqyx cujo o valor seja igual ao indice_array_atual) {
                    *            # Se for maior vamos descer ele
                    *            Click no span.MuiButtonBase-root.css-2wyiu que está dentro da div.css-z0sbrd que está dentro do pai :nth-match('div.MuiCard-root.css-xz389d, card_atual') o qual tem o h6.MuiTypography-root.css-rckqyx cujo o valor seja igual ao indice_array_atual e também o svg.MuiSvgIcon-root.css-1in44b7 com o data-testid="ArrowCircleDownIcon" * diferenca # Aqui vamos fazer com que ele repita esse click a quantidade da diferença mutiplicando ele
                    *            Passa para próxima iteração
                    *        } Senão Se (indice_array < indice da div.css-z0sbrd que está dentro do pai :nth-match('div.MuiCard-root.css-xz389d, card_atual') o qual tem o h6.MuiTypography-root.css-rckqyx cujo o valor seja igual ao indice_array_atual) {
                    *            # Se for maior vamos subir ele
                    *            Click no span.MuiButtonBase-root.css-2wyiu que está dentro da div.css-z0sbrd que está dentro do pai :nth-match('div.MuiCard-root.css-xz389d, card_atual') o qual tem o h6.MuiTypography-root.css-rckqyx cujo o valor seja igual ao indice_array_atual e também o svg.MuiSvgIcon-root.css-1in44b7 com o data-testid="ArrowCircleUpIcon" * diferenca
                    *            Passa para próxima iteração
                    *        } Senão Se (indice_array == indice da div.css-z0sbrd que está dentro do pai :nth-match('div.MuiCard-root.css-xz389d, card_atual') o qual tem o h6.MuiTypography-root.css-rckqyx cujo o valor seja igual ao indice_array_atual) {
                    *            Passa para próxima iteração # Se for igual apenas passe para a próxima iteração
                    *        }
                    
                ? ====================================== Order ====================================== ?

                    * # Sistema/Função para responder respostas do tipo Order
                    *    Pegue a resposta do arquivo JSON
                    *    Crie um array para armazenar os valores na ordem correta # Como é do tipo order (Ordenar) precisamos ter esse valores na ordem correta
                    *    Itere sobre os valores e click na ordem correta
                    *        Procure dentre as div.MuiButtonBase-root.css-16x8ql9 span.MuiChip-label.css-9iedg7 que está dentro do pai :nth-match('div.MuiCard-root.css-xz389d, card_atual') cujo valor seja igual ao ARQUIVO JSON
                    *        Click no span.MuiChip-label.css-9iedg7 que está na div.MuiButtonBase-root.css-16x8ql9 que está dentro do pai :nth-match('div.MuiCard-root.css-xz389d, card_atual') cujo valor seja igual ao ARQUIVO JSON
                    *        # Faça isso para toda a ordem

                ? ====================================== Textarea ====================================== ?
                
                    * # Sistema/Função para responder respostas do tipo Textarea
                    *    Pegue a resposta do arquivo JSON
                    *    Click no textarea.MuiInputBase-inputMultiline.css-13pivat que está no div.MuiInput-root que está dentro do pai :nth-match('div.MuiCard-root.css-xz389d, card_atual') e depois da um .fill() com o valor do JSON # Agora é apenas clicar no textarea e dar um fill (completar/encher) com a resposta do ChatGPT

                * =========================================== ***** =========================================== *

                ? Adicionar forma de verificar se todas as questões foram selecionadas 
                ? Adicionar forma de clicar no botão enviar
                ? Adicionar forma de clicar no botão Salvar rascunho
                ? Salvar as seguintes informações em um JSON
                    ? Total de atividades feitas
                    ? Adicionar forma de verificar quantas você acertou
                    ? Adicionar forma de verificar quantas você errou
                
                * =========================================== ***** =========================================== *

        """

        """
        
        Chat estou desenvolvendo uma automação usando Python e a Biblioteca Play Wright, toda a lógica já foi feita, agora estamos na parte final do código, estamos desenvolvendo uma função para identificar e responder os cards
        Chat estou desenvolvendo uma automação usando Python e a Biblioteca Play Wright a ideia é que ela responde formuláiros de uma página, o site em si é dinamico sendo gerenciado totalmente pelo JS, porém a parte do formulário não é gerenciada diretamente pelo JS. Gostaria que você explicase essa lógica para navgegar no formulário, identificar os cards e responder o mesmo.
        Chat estou desenvolvendo uma automação usando Python e a Biblioteca Play Wright a ideia é que ela responde formuláiros de uma página, o site em si é dinamico sendo gerenciado totalmente pelo JS, porém a parte do formulário não é gerenciada diretamente pelo JS. Gostaria que as linhas de códigos que eu mandar você possa converter em código Python

        """

        page.wait_for_timeout(5000)
        page.wait_for_timeout(5000)

run()