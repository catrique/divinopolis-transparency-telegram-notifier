import requests
from datetime import datetime
from playwright.sync_api import sync_playwright
import os

BOT_TOKEN = os.getenv("TELEGRAM_BOT_TOKEN")
CHAT_ID = os.getenv("TELEGRAM_CHAT_ID")
NOMES = os.getenv("NOMES_BUSCA")

if not BOT_TOKEN:
    raise ValueError("TELEGRAM_BOT_TOKEN não definido")

if not CHAT_ID:
    raise ValueError("TELEGRAM_CHAT_ID não definido")

if not NOMES:
    raise ValueError("NOMES_BUSCA não definido")

URL = "https://transparencia.betha.cloud/#/oU8BIS7tF8icFMLVMRCkJA==/consulta/83713"



def enviar_telegram(msg):
    response = requests.post(
        f"https://api.telegram.org/bot{BOT_TOKEN}/sendMessage",
        json={
            "chat_id": CHAT_ID,
            "text": msg
        },
        timeout=15
    )

    response.raise_for_status()

context = None

with sync_playwright() as p:
    browser = p.chromium.launch(headless=True)

    try:
        context = browser.new_context(
            viewport={"width": 1920, "height": 1080},
            user_agent=(
                "Mozilla/5.0 (Windows NT 10.0; Win64; x64) "
                "AppleWebKit/537.36 (KHTML, like Gecko) "
                "Chrome/124.0.0.0 Safari/537.36"
            ),
            java_script_enabled=True,
        )

        page = context.new_page()

        print("Abrindo portal...")
        page.goto(URL, wait_until="networkidle")
        page.wait_for_timeout(8000)  
        print("Clicando em Filtros...")
        filtro_btn = page.locator("button.filtro-button")
        filtro_btn.wait_for(state="visible", timeout=60000)
        filtro_btn.scroll_into_view_if_needed()
        filtro_btn.click()
        page.wait_for_timeout(2000)

        competencia = datetime.now().strftime("%m/%Y")
        # competencia = "05/2026"
        print(f"Selecionando competência: {competencia}")

        radio_label = page.locator(
            f'input[name="competencia"][value="{competencia}"] + label'
        )

        if radio_label.count() == 0:
            print("Mês não visível na lista, abrindo dropdown de alternativas...")
            page.locator("#competenciafilter a").click()
            page.wait_for_timeout(1000)

            dropdown_input = page.locator(
                "#competenciafilter .dropdown-menu input[type='text']"
            )
            dropdown_input.wait_for(state="visible", timeout=10000)
            dropdown_input.fill(competencia)
            page.wait_for_timeout(1500)

            radio_label = page.locator(
                f'input[name="competencia"][value="{competencia}"] + label'
            )

        radio_label.first.click()
        page.wait_for_timeout(1000)

        print("Confirmando filtro de competência com Enter...")
        page.keyboard.press("Enter")
        page.wait_for_timeout(4000)  

        nomes = [nome.strip() for nome in NOMES.splitlines() if nome.strip()]
        for i, NOME_BUSCA in enumerate(nomes, start=1):
            print(f"Buscando {i}/{len(nomes)}...")
            busca = page.locator('input#\\#search')
            if busca.count() == 0:
                busca = page.locator('input[placeholder="O que você está buscando?"]').first
            busca.wait_for(state="visible", timeout=30000)
            busca.click()
            busca.fill("")
            busca.fill(NOME_BUSCA)
            page.wait_for_timeout(500)
            page.keyboard.press("Enter")
            page.wait_for_timeout(2000)

        print("Aguardando resultados...")
        page.wait_for_selector(".titleValueTableColumn", timeout=30000)
        page.wait_for_timeout(2000)
        linhas = page.locator("tr:has(.titleValueTableColumn)")
        qtd = linhas.count()
        print(f"Resultados encontrados: {qtd}")
        if qtd > 0:
            dados_lista = page.evaluate("""
            () => {
                const linhas = document.querySelectorAll("tr:has(.titleValueTableColumn)");
                const resultados = [];
                linhas.forEach(linha => {
                    const resultado = {};
                    linha.querySelectorAll("td").forEach(td => {
                        const label = td.querySelector(".titleTableColumn");
                        const valor = td.querySelector(".titleValueTableColumn span");
                        if (label && valor) {
                            resultado[label.innerText.trim()] = valor.innerText.trim();
                        }
                    });
                    if (Object.keys(resultado).length > 0) resultados.push(resultado);
                });
                return resultados;
            }
        """)

        print(f"{len(dados_lista)} registros encontrados.")

        if not dados_lista:
            print("Nenhum dado extraído.")
            enviar_telegram("Erro: não foi possível extrair os dados.")
        else:
            partes = []
            liquido_total = 0
            for dados in dados_lista:
                nome    = next((v for k, v in dados.items() if "Nome"    in k), "Desconhecido")
                bruto   = next((v for k, v in dados.items() if "bruta"   in k), "")
                liquido = next((v for k, v in dados.items() if "líquida" in k or "liquida" in k), "")
                partes.append(
                    f"👤 {nome.title()}\n"
                    f"   Bruto:   {bruto}\n"
                    f"   Líquido: {liquido}"
                )

                liquido_total += float(liquido.replace("R$ ", "").replace(".", "").replace(",", "."))

            mensagem = f"📊 Rendimentos de {competencia}\n\n" + "\n\n".join(partes) + f"\n\n💰 Total Líquido: R$ {liquido_total:,.2f}"
            print("Mensagem enviada com sucesso.")
            enviar_telegram(mensagem)
    
    except Exception as e:
        try:
            enviar_telegram(f"Nenhum dado encontrado.")
        except Exception:
            pass
        raise

    finally:
        if context:
            context.close()
        browser.close()
