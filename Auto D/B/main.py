from playwright.sync_api import sync_playwright
import json


def login_estudante(page, ra, dg, uf, ps):
    """Realiza o login com as credenciais fornecidas."""
    page.locator('div#access-student').click()
    page.locator('input#ra-student').fill(ra)
    page.locator('input#digit-student').fill(dg)
    page.locator('select#uf-student').select_option(value=uf)
    page.locator('input#password-student').fill(ps)
    page.locator('input#btn-login-student').click()


def acessar_sala(page):
    """Acessa a sala de aula após o login."""
    sala = page.locator(':nth-match(div#lproom_r783fda450260e0cbe-l.lproom_r783fda450260e0cbe-l.frm.w100.p10.pt, 4)')
    sala.click()


def acessar_atividades(page):
    """Acessa a página de atividades."""
    url_atividades = "https://cmsp.ip.tv/mobile/tms?auth_token=eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJza2V5IjoiYXV0aF90b2tlbjplZHVzcDpkYW5pZWxvbGl2ZTEwMDY1OTE4My1zcCIsIm5pY2siOiJkYW5pZWxvbGl2ZTEwMDY1OTE4My1zcCIsInJvbGUiOiIwMDA2IiwicmVhbG0iOiJlZHVzcCIsImlhdCI6MTczMzUxOTYwOSwiYXVkIjoid2ViY2xpZW50In0.oqO-eR0IwyvdISxDKoKaGCsQI4dXw-3S9tUblegiV4g&room=r783fda450260e0cbe-l"
    page.goto(url_atividades)
    page.locator(':nth-match(div.MuiBox-root.css-p0pzb2, 2)').click()


def verificar_elemento_existe(page, seletor):
    """Verifica a existência de um elemento na página."""
    elemento = page.locator(seletor)
    if elemento.count() > 0:
        print("Elemento encontrado.")
        return True
    else:
        print("Elemento não encontrado.")
        return False


def rolar_ate_ultimo_item(page, seletor_atividades):
    """Rola até o último item da página de atividades."""
    atividades = page.locator(seletor_atividades)
    total_atividades = atividades.count()

    if total_atividades > 0:
        print(f"Total de atividades encontradas: {total_atividades}")
        ultimo_item = page.locator(f'{seletor_atividades}:nth-match({seletor_atividades}, {total_atividades})')
        ultimo_item.scroll_into_view_if_needed()
        print(f"Rolando até o último item (atividade {total_atividades}).")
    else:
        print("Não há atividades para rolar.")


def contar_atividades_pendentes(page, seletor_atividades):
    """Conta as atividades pendentes na página e retorna o total de atividades."""
    atividades = page.locator(seletor_atividades)
    atividades_iniciais = atividades.count()
    print(f"Atividades iniciais encontradas: {atividades_iniciais}")

    rolagem = 1
    while rolagem > 0:
        rolar_ate_ultimo_item(page, seletor_atividades)
        page.wait_for_timeout(500)

        atividades_atualizadas = atividades.count()
        if atividades_atualizadas > atividades_iniciais:
            print(f"Número de atividades aumentou: {atividades_atualizadas}")
            atividades_iniciais = atividades_atualizadas
            rolagem += 1
        else:
            print("Número de atividades não aumentou, presumindo que não há mais lições.")
            rolagem = 0

    print(f"Total de atividades encontradas: {atividades_iniciais}")
    return atividades_iniciais


def ir_para_aba_expiradas(page):
    """Vai para a aba 'Expiradas'."""
    page.locator('div#language').click()
    page.locator(':nth-match(li.css-p0z5r, 2)').click()
    print("Navegando para a aba 'Expiradas'.")


def validar_atividade_realizavel(page, seletor_botao_realizar):
    """Validar atividade"""
    botao_realizar = page.locator(seletor_botao_realizar)
    
    if botao_realizar.locator('span.css-1l6c7y9').count() > 0:
        print("A atividade NÃO pode ser realizada (Botão com span).")
        return False
    
    elif botao_realizar.inner_text() != "Realizar":
        print("A atividade NÃO pode ser realizada (Texto diferente de 'Realizar').")
        return False
    
    print("A atividade PODE ser realizada.")
    return True


card_atual = 1
texto_atual = 1
questao_atual = 1

def fazer_atividade(page, seletor_botao_realizar):
    """Fazer Atividade"""
    page.locator(seletor_botao_realizar).click()
    
    tipo_questao_1 = 'Texto'
    tipo_questao_2 = 'Radios'
    tipo_questao_3 = 'Checkbox'
    tipo_questao_4 = 'Dragable'
    tipo_questao_5 = 'Order'
    tipo_questao_6 = 'Textarea'
    #! tipo_questao_7 = 'Select'

    card_verificado = 0
    questoes_respondido = 0

    questao_texto_img_gif_video = 0
    img_gif_video = 0
    questao_texto = 0
    questao_radios = 0
    questao_checkbox = 0
    questao_dragable = 0
    questao_order = 0
    questao_textarea = 0
    #! questao_select = 0

    numero_de_card = len(page.query_selector_all('div.css-xz389d'))
    numero_de_questao = len(page.query_selector_all('div.css-nlzma4'))

    while card_verificado < numero_de_card:
            head_texto = ''
            head_questao = ''
            tipo_questao = ''
            #! alternativas_quetao = []
            card_selector = f":nth-match(div.MuiCard-root.css-xz389d, {card_atual})"

            # Verifica se o card tem PDF, Vídeo ou GIF
            if page.locator(f"{card_selector} div.css-1mi3tt8").count() > 0 or \
               page.locator(f"{card_selector} div.ytp-cued-thumbnail-overlay").count() > 0 or \
               page.locator(f"{card_selector} img[style*='max-width: 100%;']").count() > 0:
                
                if page.locator(f"{card_selector} h6.MuiTypography-root.MuiTypography-subtitle2.css-qpwa0j").count() > 0:
                    # Tem texto explicativo sobre o assunto
                    head_texto = page.locator(f"{card_selector} h6.MuiTypography-root.MuiTypography-subtitle2.css-qpwa0j").text_content().strip()
                    tipo_questao = tipo_questao_1
                    salvarJSON(tipo_questao, texto_atual, head_texto)
                    questao_texto_img_gif_video += 1
                    texto_atual += 1
                else:
                    # Tem apenas PDF/Vídeo/GIF
                    img_gif_video += 1

                # Avançar para o próximo card
                card_atual += 1
                card_verificado += 1
                continue

            # Se não for PDF/Vídeo/GIF, pode ser uma questão
            if page.locator(f"{card_selector} h6.MuiTypography-root.MuiTypography-subtitle2.css-qpwa0j").count() > 0:
                # Questão de texto
                head_questao = page.locator(f"{card_selector} h6.MuiTypography-root.MuiTypography-subtitle2.css-qpwa0j").text_content().strip()
                tipo_questao = tipo_questao_1
                salvarJSON(tipo_questao, texto_atual, head_questao)
                questao_texto += 1
                texto_atual += 1
                card_atual += 1
                card_verificado += 1
                continue

            # Identificar tipo de questão e extrair informações
            if page.locator(f"{card_selector} div.css-nlzma4").count() > 0:
                # Se for uma questão de algum tipo específico
                if page.locator(f"{card_selector} span.MuiRadios-root.css-1sgsc5r").count() > 0:
                    # Questão tipo Radio
                    questao_radios += 1
                    questao_radios_data = extrair_questao_radios(page, card_selector)

                    salvarJSON(tipo_questao_2, questao_atual, questao_radios_data['titulo'], questao_radios_data['alternativas'])

                    questoes_respondido += 1
                    questao_atual += 1
                    card_atual += 1
                    card_verificado += 1
                    continue

                elif page.locator(f"{card_selector} span.MuiCheckbox-root.css-14bgux8").count() > 0:
                    # Questão tipo Checkbox
                    questao_checkbox += 1
                    questao_checkbox_data = extrair_questao_checkbox(page, card_selector)

                    salvarJSON(tipo_questao_3, questao_atual, questao_checkbox_data['titulo'], questao_checkbox_data['alternativas'])

                    questoes_respondido += 1
                    questao_atual += 1
                    card_atual += 1
                    card_verificado += 1
                    continue

                elif page.locator(f"{card_selector} div.css-z0sbrd").count() > 0:
                    # Questão tipo Dragable
                    questao_dragable += 1
                    questao_dragable_data = extrair_questao_dragable(page, card_selector)

                    salvarJSON(tipo_questao_4, questao_atual, questao_dragable_data['titulo'], questao_dragable_data['alternativas'])

                    questoes_respondido += 1
                    questao_atual += 1
                    card_atual += 1
                    card_verificado += 1
                    continue

                elif page.locator(f"{card_selector} div.MuiChip-root.css-16x8ql9").count() > 0:
                    # Questão tipo Order
                    questao_order += 1
                    questao_order_data = extrair_questao_order(page, card_selector)

                    salvarJSON(tipo_questao_5, questao_atual, questao_order_data['titulo'], questao_order_data['alternativas'])

                    questoes_respondido += 1
                    questao_atual += 1
                    card_atual += 1
                    card_verificado += 1
                    continue

                elif page.locator(f"{card_selector} div.MuiTextField-root.css-feqhe6").count() > 0:
                    # Questão tipo Textarea
                    questao_textarea += 1
                    questao_textarea_data = extrair_questao_textarea(page, card_selector)

                    salvarJSON(tipo_questao_6, questao_atual, questao_textarea_data['titulo'])

                    questoes_respondido += 1
                    questao_atual += 1
                    card_atual += 1
                    card_verificado += 1
                    continue

            # Caso não reconheça o tipo de questão, pedimos para o usuário resolver
            print(f"Card {card_atual} não identificado. Solicitando ao usuário para resolver a questão.")
            card_atual += 1
            card_verificado += 1

    print("Atividade realizada!")

### ? FUNÇÕES JSON ? ###

atividade = {
    'contexto': '''
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

respostas = {
    'resposta': {}
}

caminho_arquivo = "JSON/teste.json"

def salvarJSON(tipo='', head_texto='', head_questao='', alternativas_quetao='', questao_atual='', texto_atual=''):
    # Dicionários para armazenar os dados de texto e questões
    texto = {}
    questoes = {}
    
    # Se o tipo for 'Texto'
    if tipo == 'Texto':
        # Adiciona um novo texto no dicionário 'texto'
        texto[f"texto_{texto_atual}"] = {
            "Tipo": tipo,
            "Texto": f'{head_texto}'  # Usa o valor de 'head_texto'
        }
        # Salva em um arquivo JSON
        with open(caminho_arquivo, 'w') as arquivo_json:
            json.dump({"texto": texto}, arquivo_json, indent=4)
    
    # Se o tipo for um dos tipos de questão (tipo_questao_1 até tipo_questao_5)
    elif tipo in ['tipo_questao_1', 'tipo_questao_2', 'tipo_questao_3', 'tipo_questao_4', 'tipo_questao_5']:
        # Adiciona uma nova questão no dicionário 'questoes'
        questoes[f"questao_{questao_atual}"] = {
            "Tipo": tipo,
            "Header": f'{head_questao}',  # Usa o valor de 'head_questao'
            "Alternativas": f'{alternativas_quetao}'  # Usa o valor de 'alternativas_quetao'
        }
        # Salva em um arquivo JSON
        with open(caminho_arquivo, 'w') as arquivo_json:
            json.dump({"questoes": questoes}, arquivo_json, indent=4)


def pegar_resposta_JSON(caminho_arquivo):
    with open(caminho_arquivo, 'r') as arquivo_json:
        respostas = json.load(arquivo_json)
    return respostas

### ? FUNÇÕES RESPONDER ? ###

def responder_radios(indice_iteracao, caminho_arquivo):
    # Pega as respostas do arquivo JSON
    respostas = pegar_resposta_JSON(caminho_arquivo)
    
    if not respostas:
        return  # Se não houver resposta, sai da função

    # Verifica se a questão do tipo "Radios" existe na resposta
    questao_id = f"questao_{indice_iteracao}"  # Exemplo: "questao_1"
    if questao_id not in respostas:
        print(f"Questão {questao_id} não encontrada no arquivo JSON.")
        return

    resposta = respostas[questao_id]["Resposta"][0]  # Assume que a resposta é um único valor
    print(f"Resposta para a questão {questao_id}: {resposta}")

    '''
    # Localiza o card da questão pelo índice (na página)
    seletor_card = f":nth-match(div.MuiCard-root.css-xz389d, {card_atual})"
    
    # Localiza o conjunto de alternativas para a questão
    alternativas = pagina.locator(f"{seletor_card} div.MuiRadiosGroup-root div.css-t1yck")

    # Itera pelas alternativas e encontra a alternativa correta
    for alternativa in alternativas.element_handles():
        # Pega o valor de cada alternativa
        valor_alternativa = alternativa.locator("text=" + resposta).text_content()
        
        if valor_alternativa == resposta:
            # Clica na alternativa correta
            input_alternativa = alternativa.locator("input.PrivateSwitchBase-input.css-1m9pwf3")
            input_alternativa.click()
            print(f"Alternativa '{resposta}' selecionada.")
            break  # Para a iteração após o clique
    '''


def responder_checkbox(indice_iteracao, caminho_arquivo):
    respostas = pegar_resposta_JSON(caminho_arquivo)
    
    if not respostas:
        return  # Se não houver resposta, sai da função

    # Verifica se a questão do tipo "Checkbox" existe na resposta
    questao_id = f"questao_{indice_iteracao}"
    if questao_id not in respostas:
        print(f"Questão {questao_id} não encontrada no arquivo JSON.")
        return

    resposta = respostas[questao_id]["Resposta"]  # A resposta pode ser uma lista (mais de uma alternativa)
    print(f"Respostas para a questão {questao_id}: {resposta}")

    '''
    # Localiza o card da questão pelo índice (na página)
    seletor_card = f":nth-match(div.MuiCard-root.css-xz389d, {card_atual})"
    
    # Localiza o conjunto de alternativas para a questão
    alternativas = pagina.locator(f"{seletor_card} div.MuiCheckbox-root div.css-t1yck")

    # Itera pelas alternativas e encontra a alternativa correta
    for valor_correto in resposta:  # Resposta é uma lista de alternativas corretas
        for alternativa in alternativas.element_handles():
            # Pega o texto ou valor da alternativa
            valor_alternativa = alternativa.locator("text=" + valor_correto).text_content()
            
            if valor_alternativa == valor_correto:
                # Clica na alternativa correta
                input_alternativa = alternativa.locator("input.PrivateSwitchBase-input.css-1m9pwf3")
                input_alternativa.click()
                print(f"Alternativa '{valor_correto}' selecionada.")
                break  # Se encontrar a alternativa correta, para de iterar pelas alternativas
    '''


def responder_dragable(indice_iteracao, caminho_arquivo):
    # Pega as respostas do arquivo JSON
    respostas = pegar_resposta_JSON(caminho_arquivo)
    
    if not respostas:
        return  # Se não houver resposta, sai da função

    # Verifica se a questão do tipo "Dragable" existe na resposta
    questao_id = f"questao_{indice_iteracao}"  # Exemplo: "questao_1"
    if questao_id not in respostas:
        print(f"Questão {questao_id} não encontrada no arquivo JSON.")
        return

    # A resposta para "Dragable" é uma lista com a ordem correta das alternativas
    resposta = respostas[questao_id]["Resposta"]
    print(f"Respostas para a questão {questao_id}: {resposta}")

    '''
    # Localiza o card da questão pelo índice (na página)
    seletor_card = f":nth-match(div.MuiCard-root.css-xz389d, {card_atual})"
    
    # Localiza as alternativas dentro do card, usando o seletor de "dragable"
    alternativas = pagina.locator(f"{seletor_card} div.css-z0sbrd")

    # Itera sobre as alternativas e organiza elas na ordem correta
    for indice_array, valor_correto in enumerate(resposta):
        # Encontramos a alternativa no DOM
        alternativa = pagina.locator(f"{seletor_card} div.css-z0sbrd h6.MuiTypography-root.css-rckqyx:text('{valor_correto}')")
        
        # Pega o índice atual da alternativa no DOM
        indice_atual = alternativas.locator(f"h6.MuiTypography-root.css-rckqyx:text('{valor_correto}')").element_handle().index()

        # Calcula a diferença de índice
        diferenca = indice_array - indice_atual
        
        # Se a alternativa está abaixo da posição desejada (mover para cima)
        if diferenca < 0:
            # Mover para cima (clicando no ícone de "ArrowCircleUpIcon")
            for _ in range(abs(diferenca)):
                mover_para_cima = alternativa.locator("span.MuiButtonBase-root.css-2wyiu svg[data-testid='ArrowCircleUpIcon']")
                mover_para_cima.click()
            print(f"Movendo '{valor_correto}' para cima.")
        
        # Se a alternativa está acima da posição desejada (mover para baixo)
        elif diferenca > 0:
            # Mover para baixo (clicando no ícone de "ArrowCircleDownIcon")
            for _ in range(abs(diferenca)):
                mover_para_baixo = alternativa.locator("span.MuiButtonBase-root.css-2wyiu svg[data-testid='ArrowCircleDownIcon']")
                mover_para_baixo.click()
            print(f"Movendo '{valor_correto}' para baixo.")
        
        # Se a alternativa já estiver na posição correta, não faz nada
        else:
            print(f"Alternativa '{valor_correto}' já está na posição correta.")
        
        # Passa para a próxima iteração
        continue
    '''


def responder_order(indice_iteracao, caminho_arquivo):
    # Pega as respostas do arquivo JSON
    respostas = pegar_resposta_JSON(caminho_arquivo)
    
    if not respostas:
        return  # Se não houver resposta, sai da função

    # Verifica se a questão do tipo "Order" existe na resposta
    questao_id = f"questao_{indice_iteracao}"  # Exemplo: "questao_1"
    if questao_id not in respostas:
        print(f"Questão {questao_id} não encontrada no arquivo JSON.")
        return

    # A resposta para "Order" é uma lista com a ordem correta
    ordem_correta = respostas[questao_id]["Resposta"]
    print(f"Ordem correta para a questão {questao_id}: {ordem_correta}")

    '''
    # Localiza o card da questão pelo índice (na página)
    seletor_card = f":nth-match(div.MuiCard-root.css-xz389d{card_atual})"
    
    # Localiza o conjunto de elementos para ordenar
    elementos = pagina.locator(f"{seletor_card} div.MuiButtonBase-root.css-16x8ql9 span.MuiChip-label.css-9iedg7")

    # Cria um array para armazenar os elementos e seus valores
    elementos_valores = []
    for elemento in elementos.element_handles():
        valor_elemento = elemento.text_content().strip()  # Pega o valor do chip
        elementos_valores.append((valor_elemento, elemento))

    # Itera sobre os valores na ordem correta
    for valor_correto in ordem_correta:
        # Procura o elemento com o valor da resposta
        for valor_elemento, elemento in elementos_valores:
            if valor_elemento == valor_correto:
                # Clica no elemento correspondente
                elemento.click()
                print(f"Elemento '{valor_correto}' selecionado.")
                break  # Sai do loop assim que encontra o valor correto
    '''


def responder_textarea(indice_iteracao, caminho_arquivo):
    # Pega as respostas do arquivo JSON
    respostas = pegar_resposta_JSON(caminho_arquivo)
    
    if not respostas:
        return  # Se não houver resposta, sai da função

    # Verifica se a questão do tipo "Textarea" existe na resposta
    questao_id = f"questao_{indice_iteracao}"  # Exemplo: "questao_1"
    if questao_id not in respostas:
        print(f"Questão {questao_id} não encontrada no arquivo JSON.")
        return

    # A resposta para "Textarea" é uma string
    resposta = respostas[questao_id]["Resposta"]
    print(f"Resposta para a questão {questao_id}: {resposta}")

    '''
    # Localiza o card da questão pelo índice (na página)
    seletor_card = f":nth-match(div.MuiCard-root.css-xz389d{card_atual})"
    
    # Localiza o campo de texto (textarea) dentro do card
    campo_texto = pagina.locator(f"{seletor_card} div.MuiInput-root textarea.MuiInputBase-inputMultiline.css-13pivat")

    # Clica no campo de texto e preenche com a resposta
    campo_texto.click()
    campo_texto.fill(resposta)
    print(f"Resposta preenchida: {resposta}")
    '''


'''#!
### ! FUNÇÃO VERIFICAR IMAGEM NAS ALTERNATIVAS ? ###

def verificar_imagens_nas_alterntativas () {
    # Supondo que 'card_atual' é um elemento Playwright com a estrutura esperada
    se (dentro da :nth-match('div.MuiCard-root.css-xz389d, card_atual')
  
    div.MuiPaper-root.css-1db9nhj > img.MuiCardMedia-root.css-5rs0y1
}

'''

### ? FUNÇÕES EXTRAIR ? ###

def extrair_titulo_do_card(page, card_selector):
    seletor = f"{card_selector} div.css-1v3caum div[style=\"padding: 0px 24px;\"]"
    texto = page.locator(seletor).text_content()
    return texto.strip()  # Retorna o texto do título da questão


def extrair_questao_radios(page, card_selector):
    # Chama a função reutilizável para extrair o título
    head_questao = extrair_titulo_do_card(page, card_selector)

    # Array para armazenar as alternativas
    alternativas_quetao = []

    # Itera sobre cada alternativa de radio dentro do card
    alternativas = page.locator(f"{card_selector} div.css-t1yck")
    numero_alternativas = alternativas.count()

    for indice_iteracao in range(1, numero_alternativas + 1):
        # Localiza a alternativa atual
        alternativa = alternativas.nth(indice_iteracao - 1)  # nth é indexado de 0
        
        # Verifica se existe uma imagem dentro da alternativa (indicando necessidade de resposta manual)
        imagem_elemento = alternativa.locator("img.MuiCardMedia-root.css-5rs0y1").first

        if imagem_elemento.is_visible():
            print("Alternativa com imagem encontrada. Pause e peça ao usuário para responder manualmente.")
            input("Pressione Enter após o usuário responder manualmente...")
            break  # Interrompe a iteração quando houver uma imagem

        else:
            # Extrai o texto da alternativa
            texto_alternativa = alternativa.locator("div.MuiBox-root.css-kmkory").text_content()
            alternativas_quetao.append(texto_alternativa.strip())  # Adiciona ao array de alternativas

    return {
        "titulo": head_questao,
        "alternativas": alternativas_quetao
    }

    '''
        # Localize o card atual (exemplo: primeiro card)
        card_atual = pagina.locator('div.MuiCard-root.css-xz389d:nth-of-type(1)')  # Exemplo de índice

        # Chame a função para extrair a questão e alternativas
        resultado = extrair_questao_radios(card_atual)
        print(f"Título da questão: {resultado['titulo']}")
        print(f"Alternativas: {resultado['alternativas']}")
    '''


def extrair_questao_checkbox(page, card_selector):
    # Chama a função reutilizável para extrair o título
    head_questao = extrair_titulo_do_card(page, card_selector)

    # Array para armazenar as alternativas
    alternativas_quetao = []

    # Itera sobre cada alternativa de checkbox dentro do card
    alternativas = page.locator(f"{card_selector} div.css-t1yck")
    numero_alternativas = alternativas.count()

    for indice_iteracao in range(1, numero_alternativas + 1):
        # Localiza a alternativa atual
        alternativa = alternativas.nth(indice_iteracao - 1)  # nth é indexado de 0
        
        # Verifica se existe uma imagem dentro da alternativa (indicando necessidade de resposta manual)
        imagem_elemento = alternativa.locator("img.MuiCardMedia-root.css-5rs0y1").first

        if imagem_elemento.is_visible():
            print("Alternativa com imagem encontrada. Pause e peça ao usuário para responder manualmente.")
            input("Pressione Enter após o usuário responder manualmente...")
            break  # Interrompe a iteração quando houver uma imagem

        else:
            # Extrai o texto da alternativa
            texto_alternativa = alternativa.locator("div.MuiBox-root.css-kmkory").text_content()
            alternativas_quetao.append(texto_alternativa.strip())  # Adiciona ao array de alternativas

    return {
        "titulo": head_questao,
        "alternativas": alternativas_quetao
    }

    '''
    # Localize o card atual (exemplo: primeiro card)
    card_atual = pagina.locator('div.MuiCard-root.css-xz389d:nth-of-type(1)')  # Exemplo de índice

    # Chame a função para extrair a questão e alternativas
    resultado = extrair_questao_checkbox(card_atual)
    print(f"Título da questão: {resultado['titulo']}")
    print(f"Alternativas: {resultado['alternativas']}")
    '''


def extrair_questao_dragable(page, card_selector):
    # Chama a função reutilizável para extrair o título
    head_questao = extrair_titulo_do_card(page, card_selector)

    # Array para armazenar as alternativas
    alternativas_quetao = []

    # Itera sobre cada alternativa dragable dentro do card
    alternativas = page.locator(f"{card_selector} div.css-z0sbrd")
    numero_alternativas = alternativas.count()

    for indice_iteracao in range(1, numero_alternativas + 1):
        # Localiza a alternativa atual
        alternativa = alternativas.nth(indice_iteracao - 1)  # nth é indexado de 0
        
        # Verifica se existe uma imagem dentro da alternativa (indicando necessidade de resposta manual)
        imagem_elemento = alternativa.locator("img.MuiCardMedia-root.css-5rs0y1").first

        if imagem_elemento.is_visible():
            print("Alternativa com imagem encontrada. Pause e peça ao usuário para responder manualmente.")
            input("Pressione Enter após o usuário responder manualmente...")
            break  # Interrompe a iteração quando houver uma imagem

        else:
            # Extrai o texto da alternativa
            texto_alternativa = alternativa.locator("div.MuiBox-root.css-16izr03").text_content()

            # Extrai o índice da alternativa, usando o atributo 'data-content'
            index = alternativa.locator("div.css-z0sbrd").get_attribute("data-content")
            if index:
                # O índice é extraído da string "Index: número_do_index"
                index_numero = int(index.split(":")[1].strip())
            else:
                index_numero = None

            alternativas_quetao.append({
                "texto": texto_alternativa.strip(),
                "index": index_numero
            })  # Adiciona a alternativa e seu índice ao array

    return {
        "titulo": head_questao,
        "alternativas": alternativas_quetao
    }

    '''
    # Localize o card atual (exemplo: primeiro card)
    card_atual = pagina.locator('div.MuiCard-root.css-xz389d:nth-of-type(1)')  # Exemplo de índice

    # Chame a função para extrair a questão e alternativas
    resultado = extrair_questao_dragable(card_atual)
    print(f"Título da questão: {resultado['titulo']}")
    print(f"Alternativas: {resultado['alternativas']}")
    '''


def extrair_questao_order(page, card_selector):
    # Chama a função reutilizável para extrair o título
    head_questao = extrair_titulo_do_card(page, card_selector)

    # Array para armazenar as alternativas
    alternativas_quetao = []

    # Itera sobre cada alternativa "Order" dentro do card
    alternativas = page.locator(f"{card_selector} div.css-16x8ql9")
    numero_alternativas = alternativas.count()

    for indice_iteracao in range(1, numero_alternativas + 1):
        # Localiza a alternativa atual
        alternativa = alternativas.nth(indice_iteracao - 1)  # nth é indexado de 0
        
        # Verifica se existe uma imagem dentro da alternativa (indicando necessidade de resposta manual)
        imagem_elemento = alternativa.locator("img.MuiCardMedia-root.css-5rs0y1").first

        if imagem_elemento.is_visible():
            print("Alternativa com imagem encontrada. Pause e peça ao usuário para responder manualmente.")
            input("Pressione Enter após o usuário responder manualmente...")
            break  # Interrompe a iteração quando houver uma imagem

        else:
            # Extrai o texto da alternativa
            texto_alternativa = alternativa.locator("span.MuiChip-label.css-9iedg7").text_content()

            alternativas_quetao.append({
                "texto": texto_alternativa.strip()
            })  # Adiciona a alternativa ao array

    return {
        "titulo": head_questao,
        "alternativas": alternativas_quetao
    }

    '''
    # Localize o card atual (exemplo: primeiro card)
    card_atual = pagina.locator('div.MuiCard-root.css-xz389d:nth-of-type(1)')  # Exemplo de índice

    # Chame a função para extrair a questão e alternativas
    resultado = extrair_questao_order(card_atual)
    print(f"Título da questão: {resultado['titulo']}")
    print(f"Alternativas: {resultado['alternativas']}")
    '''


def extrair_questao_textarea(page, card_selector):
    # Chama a função reutilizável para extrair o título
    head_questao = extrair_titulo_do_card(page, card_selector)

    # Retorna o título da questão
    return {
        "titulo": head_questao,
    }

    '''
    # Localize o card atual (exemplo: primeiro card)
    card_atual = pagina.locator('div.MuiCard-root.css-xz389d:nth-of-type(1)')  # Exemplo de índice

    # Chame a função para extrair a questão e alternativas
    resultado = extrair_questao_textarea(card_atual)
    print(f"Título da questão: {resultado['titulo']}")
    '''


#!funcao extrair_questao_select(page, card_selector) {}


def automacao_resposta(tipo_da_questao_chatgpt, tipo_questao_atual, numero_de_respostas, indice_iteracao):
    if tipo_da_questao_chatgpt == tipo_questao_atual:
        # Valida se o tipo da questão que o ChatGPT fez é o mesmo da original
        if tipo_da_questao_chatgpt == 'tipo_questao_1':  # Rádio
            if numero_de_respostas == 1:
                responder_radios(indice_iteracao)
            else:
                input(f"Verifique a questão {indice_iteracao} e pressione Enter para continuar...")

        elif tipo_da_questao_chatgpt == 'tipo_questao_2':  # Checkbox
            if numero_de_respostas >= 1:
                responder_checkbox(indice_iteracao)
            else:
                input(f"Verifique a questão {indice_iteracao} e pressione Enter para continuar...")

        elif tipo_da_questao_chatgpt == 'tipo_questao_3':  # Drag-and-Drop
            if numero_de_respostas >= 1:
                responder_dragable(indice_iteracao)
            else:
                input(f"Verifique a questão {indice_iteracao} e pressione Enter para continuar...")

        elif tipo_da_questao_chatgpt == 'tipo_questao_4':  # Ordem
            if numero_de_respostas >= 1:
                responder_order(indice_iteracao)
            else:
                input(f"Verifique a questão {indice_iteracao} e pressione Enter para continuar...")

        elif tipo_da_questao_chatgpt == 'tipo_questao_5':  # Textarea
            if numero_de_respostas >= 1:
                responder_textarea(indice_iteracao)
            else:
                input(f"Verifique a questão {indice_iteracao} e pressione Enter para continuar...")

        else:
            input(f"Verifique a questão {indice_iteracao} e pressione Enter para continuar...")

    else:
        input(f"Verifique a questão {indice_iteracao} e pressione Enter para continuar...")

    '''
    # Exemplificando como o código seria executado
    tipo_da_questao_chatgpt = 'tipo_questao_1'
    tipo_questao_atual = 'tipo_questao_1'
    numero_de_respostas = 1
    indice_iteracao = 1

    # Aqui você pode pegar o tipo de questão diretamente da página usando Playwright,
    # como por exemplo pegar os tipos dos elementos com seletores CSS.

    # Exemplo de seleção do tipo da questão:
    # tipo_da_questao_chatgpt = page.query_selector('div.MuiCard-root.css-xz389d div.css-1v3caum').inner_text()

    # Executar a automação de respostas
    automacao_resposta(tipo_da_questao_chatgpt, tipo_questao_atual, numero_de_respostas, indice_iteracao)
    '''


def clicar_atividade(page, seletor_atividade):
    """Clica na atividade"""
    
    atividade_btn = page.locator(seletor_atividade)
    
    atividade_btn.scroll_into_view_if_needed()
    
    atividade_btn.wait_for(state="visible")
    
    atividade_btn.click()
    print("Atividade clicada.")


""" RUN """


def run(ra, dg, uf, ps):
    """Função principal para executar o fluxo do bot."""
    with sync_playwright() as p:
        browser = p.chromium.launch(headless=False)
        page = browser.new_page()
        page.goto("https://cmspweb.ip.tv/login")
        
        login_estudante(page, ra, dg, uf, ps)
        acessar_sala(page)
        acessar_atividades(page)
        
        seletor_tabela = 'table.MuiTable-root.css-1rb4ifj'
        seletor_atividades = 'button.css-k9aczr'
        seletor_botao_realizar = 'button.css-1hmr1hq'
        
        if verificar_elemento_existe(page, seletor_tabela):
            print("Existem lições para realizar.")
            atividades_pendentes = contar_atividades_pendentes(page, seletor_atividades)
            print(f"Há {atividades_pendentes} atividades pendentes para realizar na aba 'A fazer'.")
            
            for i in range(1, atividades_pendentes + 1):
                seletor_atividade = f":nth-match({seletor_atividades}, {i})"
                
                clicar_atividade(page, seletor_atividade)
                
                page.wait_for_selector(seletor_botao_realizar)
                
                if validar_atividade_realizavel(page, seletor_botao_realizar):
                    fazer_atividade(page, seletor_botao_realizar)
                else:
                    print("Atividade não pode ser realizada. Fechando o modal...")
                    page.locator(seletor_atividade).click()
                    page.wait_for_timeout(500)
        else:
            print("Não há lições na aba 'A fazer'. Navegando para a aba 'Expiradas'.")
            ir_para_aba_expiradas(page)
            print("Verificando novamente na aba 'Expiradas'...")
            page.wait_for_selector(seletor_tabela)
            
            if verificar_elemento_existe(page, seletor_tabela):
                print("Existem lições na aba 'Expiradas'.")
                atividades_pendentes = contar_atividades_pendentes(page, seletor_atividades)
                print(f"Há {atividades_pendentes} atividades pendentes para realizar na aba 'Expiradas'.")
                
                for i in range(1, atividades_pendentes + 1):
                    seletor_atividade = f":nth-match({seletor_atividades}, {i})"
                    
                    clicar_atividade(page, seletor_atividade)
                    
                    page.wait_for_selector(seletor_botao_realizar)
                    
                    if validar_atividade_realizavel(page, seletor_botao_realizar):
                        fazer_atividade(page, seletor_botao_realizar)
                    else:
                        print("Atividade não pode ser realizada. Fechando o modal...")
                        page.locator(seletor_atividade).click()
                        page.wait_for_timeout(500)
            else:
                print("Não há lições na aba 'Expiradas'.")
        
        page.wait_for_timeout(5000)
        browser.close()

# Dados para o login
if __name__ == '__main__':
    ra = "110065918"
    dg = "3"
    uf = "SP"
    ps = "Bp110065#"
    run(ra, dg, uf, ps)
    