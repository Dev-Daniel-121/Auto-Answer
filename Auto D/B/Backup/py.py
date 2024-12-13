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
                TODO Armazenar conteúdo em um arquivo JSON já preparado                                                     ✔
                TODO Escolher AI para responder (Sugestões: GPT-Neox ou GPT-J)                                              ✔ ✖
                    ? Primeira IDEIA: GPT-J, por ser mais leve
                TODO Escolher API para alimentar a AI (Sugestões: Google Custom Search API, Bing Search API ou SerpAPI)     ✔ ✖
                    ? Primeira IDEIA: SerpAPI, por possui até 5000 buscas p/ mês e possibilidade de integração com outros motores de buscas
                
                ??? ========================================= ***** ========================================= ???

                card_atual = 1 # Identificar o card atual e facilitar a especificação dos elementos dentro dela
                texto_atual = 1 # Identificar o texto atual e facilitar a especificação dos elementos dentro dela
                questao_atual = 1 # Identificar a questão atual e facilitar a especificação dos elementos dentro dela

                card_verificado = 0 # Será para ajudar na verificação final
                questoes_respondido = 0 # Número de questões respondidas

                # Essas variaveis vão servir para ajudar a contar e a entender quais questões aparecem mais
                questao_texto_img_gif_video = 0
                img_gif_video = 0
                questao_texto = 0
                questao_radios = 0
                questao_checkbox = 0
                questao_dragable = 0
                questao_order = 0
                questao_textarea = 0
                #! questao_select = 0
                
                ## DESCOBRIR QUANTAS VERIFICAÇÕES TEM QUE FAZER
                numero_de_card = número de div.css-xz389d # A div.css-xz389d são cada card
                numero_de_questao = número de div.css-nlzma4 # A div.css-nlzma4 são cada card de questões
                
                # JSON
                atividade = {
                    contexto: ''''''
                }
                respostas = {
                    contexto: ''''''
                    resposta = {
                        resposta_GPT
                    }
                }

                funcao salvarJSON(tipo='', head_texto='', head_questao='', alternativas_quetao='', questao_atual='', texto_atual=''):
                    se (tipo == 'Texto')
                        atividade = {
                            texto[f"texto_{texto_atual}"] = { # O $ é o valor da texto_atual
                                Tipo: tipo,
                                Texto: f'''head_texto''' # Troque ''' por aspas duplas
                            }
                        }
                    senao se (tipo == 'Radios' ou tipo == 'Checkbox' ou tipo == 'Dragable' ou tipo == 'Order' ou tipo == 'Textarea') {
                        atividade = {
                            questoes[f"questao_{questao_atual}"] = { # O $ é o valor da questao_atual
                                Tipo: tipo,
                                Header: f'''{head_questao}''',
                                Alternativas = f'''{alternativas_quetao}'''
                            }
                        }
                    }
                
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
                            head_texto = Todo o conteúdo do :nth-match('h6.MuiTypography-root.MuiTypography-subtitle2.css-qpwa0j, texto_atual') pegue todo e qualquer forma de Texto
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
                                    head_questao = Todo o conteúdo da div com o atributo style="padding: 0px 24px;" que está dentro da div.css-1v3caum que está dentro do pai que é :nth-match('div.MuiCard-root.css-xz389d, card_atual') pegue todo e qualquer forma de Texto # Isso é para garantir que vamos pegar todo o conteúdo do título da questão
                                    tipo = 'Radios'
                                    alternativas_quetao = []
                                    Itere sobre cada div.css-t1yck que está dentro do pai que é :nth-match('div.MuiCard-root.css-xz389d, card_atual') e guarde no array alternativas_quetao
                                        Pegue o todo e qualquer forma de Texto da div.MuiBox-root.css-kmkory que está dentro da div.css-t1yck que está dentro do pai que é :nth-match('div.MuiCard-root.css-xz389d, card_atual') # Isso é para garantir que vamos pegar todo o conteúdo da alternativa atual
                                        Salve no array e passe para próxima iteração

                                    # Armazene todo esse conteúdo no dicionário para depois passar para o JSON
                                    salvarJSON(tipo, questao_atual, head_questao, alternativas_quetao)

                                    questoes_respondido += 1 # Vamos adicionar mais 1 ao número de questões respondidas
                                    questao_atual += 1
                                    questao_radios += 1
                                    Para e passa para a próxima pergunta
                                *} SENÃO SE (dentro da :nth-match('div.MuiCard-root.css-xz389d, card_atual') EXISTI span.MuiCheckbox-root.css-14bgux8) {
                                    # Se existir então é uma questão de tipo Checkbox
                                    card_verificado += 1
                                    head_questao = Todo o conteúdo da div com o atributo style="padding: 0px 24px;" que está dentro da div.css-1v3caum que está dentro do pai que é :nth-match('div.MuiCard-root.css-xz389d, card_atual') pegue todo e qualquer forma de Texto # Isso é para garantir que vamos pegar todo o conteúdo do título da questão
                                    tipo = 'Checkbox'
                                    alternativas_quetao = []
                                    Itere sobre cada div.css-t1yck que está dentro do pai que é :nth-match('div.MuiCard-root.css-xz389d, card_atual') e guarde no array alternativas_quetao
                                        Pegue o todo e qualquer forma de Texto da div.MuiBox-root.css-kmkory que está dentro da div.css-t1yck que está dentro do pai que é :nth-match('div.MuiCard-root.css-xz389d, card_atual') # Isso é para garantir que vamos pegar todo o conteúdo da alternativa atual
                                        Salve no array e passe para próxima iteração

                                    # Armazene todo esse conteúdo no dicionário para depois passar para o JSON
                                    salvarJSON(tipo, questao_atual, head_questao, alternativas_quetao)

                                    questoes_respondido += 1
                                    questao_atual += 1
                                    questao_checkbox += 1
                                    Para e passa para a próxima pergunta
                                *} SENÃO SE (dentro da :nth-match('div.MuiCard-root.css-xz389d, card_atual') EXISTI span.MuiCheckbox-root.css-14bgux8) {
                                    # Se existir então é uma questão de tipo Dragable
                                    card_verificado += 1
                                    head_questao = Todo o conteúdo da div com o atributo style="padding: 0px 24px;" que está dentro da div.css-1v3caum que está dentro do pai que é :nth-match('div.MuiCard-root.css-xz389d, card_atual') pegue todo e qualquer forma de Texto # Isso é para garantir que vamos pegar todo o conteúdo do título da questão
                                    tipo = 'Dragable'
                                    alternativas_quetao = []
                                    Itere sobre cada div.css-z0sbrd que está dentro do pai que é :nth-match('div.MuiCard-root.css-xz389d, card_atual') e guarde no array alternativas_quetao
                                        Pegue o todo e qualquer forma de Texto da div.MuiBox-root.css-16izr03 que está dentro da div.css-z0sbrd que está dentro do pai que é :nth-match('div.MuiCard-root.css-xz389d, card_atual') e também dentro de cada div.css-z0sbrd tem o data-content que dentro dele tem o "Index: número_do_index" pegue também o seu index # Isso é para garantir que vamos pegar todo o conteúdo da alternativa atual e o seu index que é a posição dela
                                        Salve no array e passe para próxima iteração

                                    # Armazene todo esse conteúdo no dicionário para depois passar para o JSON
                                    salvarJSON(tipo, questao_atual, head_questao, alternativas_quetao)

                                    questoes_respondido += 1
                                    questao_atual += 1
                                    questao_dragable += 1
                                    Para e passa para a próxima pergunta
                                *} SENÃO SE (dentro da :nth-match('div.MuiCard-root.css-xz389d, card_atual') EXISTI div.MuiChip-Default.css-16x8ql9) {
                                    # Se existir então é uma questão de tipo Order
                                    card_verificado += 1
                                    head_questao = Todo o conteúdo da div com o atributo style="padding: 0px 24px;" que está dentro da div.css-1v3caum que está dentro do pai que é :nth-match('div.MuiCard-root.css-xz389d, card_atual') pegue todo e qualquer forma de Texto # Isso é para garantir que vamos pegar todo o conteúdo do título da questão
                                    tipo = 'Order'
                                    alternativas_quetao = []
                                    Itere sobre cada div.MuiChip-root.css-16x8ql9 que está dentro do pai que é :nth-match('div.MuiCard-root.css-xz389d, card_atual') e guarde no array alternativas_quetao
                                        Pegue o todo e qualquer forma de Texto do span.MuiChip-label.css-9iedg7 que está dentro da div.MuiChip-root.css-16x8ql9 que está dentro do pai que é :nth-match('div.MuiCard-root.css-xz389d, card_atual') # Isso é para garantir que vamos pegar todo o conteúdo da alternativa atual
                                        Salve no array e passe para próxima iteração
                                    
                                    # Armazene todo esse conteúdo no dicionário para depois passar para o JSON
                                    salvarJSON(tipo, questao_atual, head_questao, alternativas_quetao)

                                    questoes_respondido += 1
                                    questao_atual += 1
                                    questao_order += 1
                                    Para e passa para a próxima pergunta
                                *} SENÃO SE (dentro da :nth-match('div.MuiCard-root.css-xz389d, card_atual') EXISTI div.MuiTextField-root.css-feqhe6) {
                                    # Se existir então é uma questão de tipo Textarea
                                    card_verificado += 1
                                    head_questao = Todo o conteúdo da div com o atributo style="padding: 0px 24px;" que está dentro da div.css-1v3caum que está dentro do pai que é :nth-match('div.MuiCard-root.css-xz389d, card_atual') pegue todo e qualquer forma de Texto # Isso é para garantir que vamos pegar todo o conteúdo do título da questão
                                    
                                    # Armazene todo esse conteúdo no dicionário para depois passar para o JSON
                                    salvarJSON(tipo, questao_atual, head_questao)
                                    
                                    questoes_respondido += 1
                                    questao_atual += 1
                                    textarea += 1
                                    Para e passa para a próxima pergunta
                                !} SENÃO SE (dentro da :nth-match('div.MuiCard-root.css-xz389d, card_atual') EXISTI span.MuiRadios-root.css-1sgsc5r) {                                }
                            }
                        }
                        VERIFICAR LIÇÃO SE AS ALTERNATIVAS FOR APENAS IMAGENS
                            PEDIR AO USUÁRIO PARA QUERESOLVA ESSA QUESTÃO E DIGA SE JÁ RESPONDEU PARA PASSAR PARA PRÓXIMA
                        PEGA O TÍTULO DA QUESTÃO E AS ALTERNATIVAS DEPOIS ARMARZENA-LÁS NO JSON
                        PEGA O JSON COM A PERGUNTA E AS ALTERNATIVAS DA questao_atual E PASSE PARA ChatGPT PARA QUE RESOLVA E RETORNE A RESPOSTA(s)
                        PEGA AS RESPOSTAS DESSE JSON E COLOUQE NA ALTERNATIVA CORRETA
                    }
                } ENQUANTO (numero_de_card > card_verificado)

                ? ====================================== Radio ====================================== ?
                
                    ?# Sistema/Função para procurar respostas
                    ?    Abra uma nova guia
                    ?    Entre em https://chatgpt.com/)
                    ?    Pega todo o conteúdo do JSON e coloca no ChatGPT
                    ?    resposta_GPT = Pege a reposta do ChtGPT
                    ?    respostas = { # Salvar no arquivo JSON para resposta
                    ?        resposta_GPT
                    ?    }
                    ?# Sistema/Função para responder respostas do tipo Radios
                    ?    Pegue a resposta do arquivo JSON
                    ?    Procure dentre as div.MuiRadiosGroup-root div.css-t1yck que estão dentro do pai :nth-match('div.MuiCard-root.css-xz389d, card_atual') uma que o valor seja igual ao ARQUIVO JSON # Essa especificação 'div.MuiRadiosGroup-root div.css-t1yck' é o conjunto de alternativas. Aqui a ideia é procurar dentro do card atual no conjunto de alternativas a alternativa que tem o valor igual ao do arquivo JSON com a resposta do ChatGPT
                    ?    Click no input.PrivateSwitchBase-input.css-1m9pwf3 que está na div.MuiRadiosGroup-root div.css-t1yck que esá dentro do pai :nth-match('div.MuiCard-root.css-xz389d, card_atual') cujo valor seja igual ao ARQUIVO JSON # Agora é apenas clicar no Input da alternativa

                ? ====================================== Checkbox ====================================== ?

                        ?# Sistema/Função para procurar respostas
                        ?    Vá para a página do ChatGPT (Abra uma nova guia, Entre em https://chatgpt.com/)
                        ?    Pega todo o conteúdo do JSON e coloca no ChatGPT
                        ?    Pega a resposta do ChatGPT que vai vim em formato JSON e armazene em outro arquivo JSON
                        ?# Sistema/Função para responder respostas do tipo Radios
                        ?    Pegue a resposta do arquivo JSON
                        ?    Crie um array com as alternativas corretas (Idependente se for apenas 1 ou mais) # Como é do tipo checkbox é possível ter mais de uma alternativa certa
                        ?    Itere sobre os valores e click na ordem correta # Iteraremos nesse array para por as respostas corretas
                        ?        Procure dentre as div.MuiCheckbox-root div.css-t1yck que está dentro do pai :nth-match('div.MuiCard-root.css-xz389d, card_atual') cujo valor seja igual ao ARQUIVO JSON
                        ?        Click no input.PrivateSwitchBase-input.css-1m9pwf3 que está na div.MuiCheckbox-root div.css-t1yck que está dentro do pai :nth-match('div.MuiCard-root.css-xz389d, card_atual') cujo valor seja igual ao ARQUIVO JSON

                ? ====================================== Dragable ====================================== ?

                        ?# Sistema/Função para responder respostas do tipo Radios
                        ?    Pegue a resposta do arquivo JSON
                        ?    Crie um array para conter as alternativas na ordem correta
                        ?    Itere sobre os valores
                        ?        Procure dentre as div.css-z0sbrd que está dentro do pai :nth-match('div.MuiCard-root.css-xz389d, card_atual') o h6.MuiTypography-root.css-rckqyx cujo o valor seja igual ao valor do indice_array_atual
                        ?        diferenca = 0 # A diferença vai começar em 0 para cada iteração
                        ?        diferenca = indice_array - indice da div.css-z0sbrd que está dentro do pai :nth-match('div.MuiCard-root.css-xz389d, card_atual') o qual tem o h6.MuiTypography-root.css-rckqyx cujo o valor seja igual ao indice_array_atual # A diferença vai servir para saber quanto precisamos subir, descer ou ficar
                        ?        Se (indice_array > indice da div.css-z0sbrd que está dentro do pai :nth-match('div.MuiCard-root.css-xz389d, card_atual') o qual tem o h6.MuiTypography-root.css-rckqyx cujo o valor seja igual ao indice_array_atual) {
                        ?            # Se for maior vamos descer ele
                        ?            Click no span.MuiButtonBase-root.css-2wyiu que está dentro da div.css-z0sbrd que está dentro do pai :nth-match('div.MuiCard-root.css-xz389d, card_atual') o qual tem o h6.MuiTypography-root.css-rckqyx cujo o valor seja igual ao indice_array_atual e também o svg.MuiSvgIcon-root.css-1in44b7 com o data-testid="ArrowCircleDownIcon" * diferenca # Aqui vamos fazer com que ele repita esse click a quantidade da diferença mutiplicando ele
                        ?            Passa para próxima iteração
                        ?        } Senão Se (indice_array < indice da div.css-z0sbrd que está dentro do pai :nth-match('div.MuiCard-root.css-xz389d, card_atual') o qual tem o h6.MuiTypography-root.css-rckqyx cujo o valor seja igual ao indice_array_atual) {
                        ?            # Se for maior vamos subir ele
                        ?            Click no span.MuiButtonBase-root.css-2wyiu que está dentro da div.css-z0sbrd que está dentro do pai :nth-match('div.MuiCard-root.css-xz389d, card_atual') o qual tem o h6.MuiTypography-root.css-rckqyx cujo o valor seja igual ao indice_array_atual e também o svg.MuiSvgIcon-root.css-1in44b7 com o data-testid="ArrowCircleUpIcon" * diferenca
                        ?            Passa para próxima iteração
                        ?        } Senão Se (indice_array == indice da div.css-z0sbrd que está dentro do pai :nth-match('div.MuiCard-root.css-xz389d, card_atual') o qual tem o h6.MuiTypography-root.css-rckqyx cujo o valor seja igual ao indice_array_atual) {
                        ?            Passa para próxima iteração # Se for igual apenas passe para a próxima iteração
                        ?        }
                    
                ? ====================================== Order ====================================== ?

                        ?# Sistema/Função para responder respostas do tipo Radios
                        ?    Pegue a resposta do arquivo JSON
                        ?    Crie um array para armazenar os valores na ordem correta # Como é do tipo order (Ordenar) precisamos ter esse valores na ordem correta
                        ?    Itere sobre os valores e click na ordem correta
                        ?        Procure dentre as div.MuiButtonBase-root.css-16x8ql9 span.MuiChip-label.css-9iedg7 que está dentro do pai :nth-match('div.MuiCard-root.css-xz389d, card_atual') cujo valor seja igual ao ARQUIVO JSON
                        ?        Click no span.MuiChip-label.css-9iedg7 que está na div.MuiButtonBase-root.css-16x8ql9 que está dentro do pai :nth-match('div.MuiCard-root.css-xz389d, card_atual') cujo valor seja igual ao ARQUIVO JSON
                        ?        # Faça isso para toda a ordem

                ? ====================================== Textarea ====================================== ?
                
                        ?# Sistema/Função para responder respostas do tipo Radios
                        ?    Pegue a resposta do arquivo JSON
                        ?    Click no textarea.MuiInputBase-inputMultiline.css-13pivat que está no div.MuiInput-root que está dentro do pai :nth-match('div.MuiCard-root.css-xz389d, card_atual') e depois da um .fill() com o valor do JSON # Agora é apenas clicar no textarea e dar um fill (completar/encher) com a resposta do ChatGPT

                * Adicionar forma de verificar se todas as questões foram selecionadas 
                * Adicionar forma de clicar no botão enviar
                * Adicionar forma de clicar no botão Salvar rascunho
                * Adicionar forma de verificar quantas você acertou
                * Adicionar forma de verificar quantas você errou
                
                * =========================================== ***** =========================================== *

                from playwright.sync_api import sync_playwright
                import json

                # Função para armazenar dados em um arquivo JSON
                def armazenar_json(arquivo, dados):
                    with open(arquivo, 'w') as f:
                        json.dump(dados, f)

                # Função para interagir com o site e resolver o formulário
                def automatizar_formulario(page):
                    questao_atual = 0
                    texto_atual = 0
                    card_verificado = 0
                    questoes_respondido = 0

                    # Descobrir quantos cards existem
                    numero_de_card = len(page.query_selector_all("div.css-xz389d"))

                    # Iniciar o loop para processar os cards
                    while numero_de_card > card_verificado:
                        card_atual = page.query_selector(f"div.css-xz389d:nth-of-type({card_verificado + 1})")

                        if card_atual:
                            # Verificar se o card contém vídeo, PDF ou GIF
                            if card_atual.query_selector("div.css-1mi3tt8") or card_atual.query_selector("div.ytp-cued-thumbnail-overlay") or card_atual.query_selector(""):
                                # Caso o card tenha conteúdo multimídia (PDF, Vídeo ou GIF)
                                if card_atual.query_selector("h6.MuiTypography-root.MuiTypography-subtitle2.css-qpwa0j"):
                                    # Se tiver texto explicativo
                                    texto_atual += 1  # Incrementa apenas quando o texto for encontrado
                                    card_verificado += 1  # Incrementa somente quando o card for processado completamente
                                    # Extrair texto dos parágrafos e armazenar
                                    textos = card_atual.query_selector_all("p")
                                    conteudo_texto = [texto.inner_text() for texto in textos]
                                    armazenar_json("textos.json", conteudo_texto)
                                else:
                                    card_verificado += 1  # Incrementa apenas quando o card multimídia for processado
                            else:
                                # Se o card não tem conteúdo multimídia, verificar se é um card de texto
                                if card_atual.query_selector("h6.MuiTypography-root.MuiTypography-subtitle2.css-qpwa0j"):
                                    texto_atual += 1  # Incrementa apenas quando o card contém texto
                                    card_verificado += 1
                                    # Extrair texto dos parágrafos e armazenar
                                    textos = card_atual.query_selector_all("p")
                                    conteudo_texto = [texto.inner_text() for texto in textos]
                                    armazenar_json("textos.json", conteudo_texto)
                                else:
                                    # Caso o card seja uma questão (ex: múltipla escolha)
                                    if card_atual.query_selector("div.css-nlzma4"):
                                        questao_atual += 1  # Incrementa somente quando uma nova questão é encontrada
                                        card_verificado += 1
                                        alternativas = card_atual.query_selector_all("div.MuiBox-root.css-kmkory p")
                                        alternativas_texto = [alt.inner_text() for alt in alternativas]
                                        armazenar_json("alternativas.json", alternativas_texto)
                                        
                                        # Simulação de busca pela resposta no ChatGPT (substitua com uma chamada real)
                                        resposta_chatgpt = {"resposta": "Alternativa A"}  # Exemplo de resposta, substitua conforme necessário
                                        
                                        # Selecionar a alternativa correta com base na resposta do ChatGPT
                                        alternativa_correta = card_atual.query_selector(f"div.MuiRadiosGroup-root div.css-t1yck input[value='{resposta_chatgpt['resposta']}']")
                                        if alternativa_correta:
                                            alternativa_correta.click()
                                            questoes_respondido += 1  # Incrementa quando uma questão é respondida
                                        card_verificado += 1

                                # Função principal que inicia a automação
                                def run():
                                    with sync_playwright() as p:
                                        browser = p.chromium.launch(headless=False)  # Você pode mudar para headless=True se quiser rodar sem interface gráfica
                                        page = browser.new_page()

                                        # Acessar o site onde o formulário está localizado
                                        page.goto("URL_DO_SEU_SITE")  # Substitua pelo URL do seu site com o formulário

                                        # Chama a função que faz a automação do formulário
                                        automatizar_formulario(page)

                                        # Fechar o navegador após o processo
                                        browser.close()

                                # Chamar a função run() para iniciar a automação
                                if __name__ == "__main__":
                                    run()

        '''
            FACA {
                SE (EXISTI a div.css-1iovhr3) { ## OU SEJA, significa que não há nada apenas um SVG para mostrar que não há nada
                    Vá para expiradas (CLICK na div#language SELECIONE a li cujo data-value="expired:all") ## VÁ para próxima seção
                } senão {
                    SABER quantos button.css-k9aczr TEM e coloque na variavel Atividades ## SABER quantos button.css-k9aczr tem, ajuda nós a identificar quantas ATIVIDADES tem para fazer
                    CLICK no PRIMEIRO button.css-k9aczr e BUSQUE por btn.css-1hmr1hq ## CLICAMOS para abrir a div e validar se dá ou não para realizar a atividade
                    SE (
                        dentro da div.css-nzomx6 no btn.css-1hmr1hq tiver span.css-1l6c7y9 ## Se há esse span NÃO DÁ PARA REALIZAR A ATIVIDADE
                        OU
                        O conteúdo do btn.css-1hmr1hq for ! de "Realizar") { # SE o TEXTO do botão for diferente então não dá para REALIZAR
                    ) {
                        CLICK no PRÓXIMO button.css-k9aczr e BUSQUE por btn.css-1hmr1hq  # Se tudo acima for verdade, vamos passar para o proximo botão e refazer os mesmos passos
                    } SE NÃO { # Se as afirmações acima forem falso, então significa que é uma ATIVIDADE e dá para REALIZAR
                        Subtraia -1 nas ativadades # Subtrair 1 das atividades para o programa saber quantas atividades ainda faltam
                        Click no btn.css-1hmr1hq # Clicar no botão para realizar
                    }
                }
            } ENQUANTO(Atividades > 0) # Faça tudo isso enquanto ainda tiver atividades
        '''
        """

        """
        
        Chat estou desenvolvendo uma automação usando Python e a Biblioteca Play Wright, toda a lógica já foi feita, agora estamos na parte final do código, estamos desenvolvendo uma função para identificar e responder os cards
        Chat estou desenvolvendo uma automação usando Python e a Biblioteca Play Wright a ideia é que ela responde formuláiros de uma página, o site em si é dinamico sendo gerenciado totalmente pelo JS, porém a parte do formulário não é gerenciada diretamente pelo JS. Gostaria que você explicase essa lógica para navgegar no formulário, identificar os cards e responder o mesmo.

        """

        page.wait_for_timeout(5000)
        page.wait_for_timeout(5000)

run()