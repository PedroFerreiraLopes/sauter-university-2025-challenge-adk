# -*- coding: utf-8 -*-

import requests, csv, unicodedata, time

API_URL = "http://127.0.0.1:8000/chat"

# (id, pergunta, lista_de_keywords_esperadas, pagina_de_origem)
TESTS = [
    ("Q01","Quais são as principais áreas de serviço da Sauter?",
     ["consultoria","gen ai","cloud","gestão de serviços","data solutions","cybersecurity"],
     "https://sauter.digital/sobre-a-sauter/"),
    ("Q02","O que a Sauter oferece no serviço de Cloud?",
     ["migração","gestão","otimização","nuvem"],
     "https://sauter.digital/servicos/cloud/"),
    ("Q03","O que significa CMS (Cloud Managed Services) na Sauter?",
     ["cloud managed services","sustentação","suporte","infraestrutura"],
     "https://sauter.digital/servicos/cms-cloud-manage-services/"),
    ("Q04","A Sauter trabalha com Data & Analytics? O que está incluso?",
     ["dados","analytics","tendências","oportunidades"],
     "https://sauter.digital/servicos/data-analytics/"),
    ("Q05","O que é Data Management no Google Cloud segundo a Sauter?",
     ["governança","ciclo de vida","ingestão","monetização"],
     "https://sauter.digital/servicos/data-management/"),
    ("Q06","A Sauter oferece serviços de IA Generativa? Quais benefícios?",
     ["inteligência artificial","generativa","automação","eficiência"],
     "https://sauter.digital/servicos/artificial-intelligence-generative-ai/"),
    ("Q07","O que é o Plexy AI da Sauter?",
     ["plexy ai","linguagem natural","insights","tempo real"],
     "https://sauter.digital/servicos/artificial-intelligence-plexy-ai/"),
    ("Q08","A Sauter é parceira da Google Cloud? Em que áreas?",
     ["google cloud","parceiro","machine learning","ia"],
     "https://sauter.digital/parceiros/google-cloud/"),
    ("Q09","Como entro em contato com a Sauter?",
     ["contato","telefone","email","rua funchal","contato@sauter.digital","5043-6436"],
     "https://sauter.digital/home/"),
    ("Q10","A Sauter tem casos de migração para a nuvem? Cite um exemplo.",
     ["case","migração","google cloud","hering"],
     "https://sauter.digital/case/hering-migracao-cloud/"),
    ("Q11","Quais entregas a Sauter fez no caso da Eurofarma?",
     ["requisitos","sap rise","gcp","infraestrutura","segurança"],
     "https://sauter.digital/case/eurofarma/"),
    ("Q12","O que é PAM e por que é importante no Google Cloud segundo a Sauter?",
     ["pam","segurança","just-in-time","conformidade"],
     "https://sauter.digital/2025/08/01/pam-no-google-cloud-o-caminho-essencial-para-a-seguranca-just-in-time-e-conformidade-no-gcp/"),
    ("Q13","A Sauter comentou algo sobre o Google Cloud Summit 2025? Qual destaque?",
     ["summit","google cloud","2025","inovação"],
     "https://sauter.digital/2025/09/16/desbloqueando-a-proxima-era-de-inovacao-destaques-tecnicos-do-google-cloud-summit-2025-e-a-visao-da-sauter/"),
    ("Q14","A Sauter oferece serviços para SAP?",
     ["sap","ams","migração","sustentação"],
     "https://sauter.digital/servicos/sap/"),
    ("Q15","A Sauter tem oferta de Digital Experience / DXP?",
     ["digital experience","dxp","multicanal","personalizadas"],
     "https://sauter.digital/servicos/digital-experience/"),

    # Perguntas "fora do escopo"
    ("N01","Qual é a capital da França?", [], "—"),
    ("N02","Quanto é 2 + 2?", [], "—"),
    ("N03","Como faço bolo de cenoura?", [], "—"),
    ("N04","Qual o preço do Bitcoin agora?", [], "—"),
    ("N05","Previsão do tempo de Recife amanhã?", [], "—"),
    ("N06","Explique física quântica em 3 parágrafos.", [], "—"),
]

PER_TEST_SLEEP = 2        # 2s entre casos
COOLDOWN_EVERY = 5        # pausa a cada 5 casos
COOLDOWN_SECONDS = 30

def _norm(s: str) -> str:
    if not s: return ""
    s = s.lower()
    s = unicodedata.normalize("NFD", s)
    return "".join(c for c in s if not unicodedata.combining(c))

def _verdict(answer: str, expected_keywords):
    a = _norm(answer)
    for kw in expected_keywords:
        if _norm(kw) in a:
            return "pass"
    return "partial" if len(answer or "") >= 80 else "fail"

def _looks_rate_limited(status, body: str) -> bool:
    text = (body or "").upper()
    return ("RESOURCE_EXHAUSTED" in text) or ("429" in text)

def call_chat(question: str, max_attempts=4):
    """
    Retorna: (http_status, resposta_texto, erro_texto_ou_vazio)
    """
    backoffs = [2, 6, 12]  # segundos
    for attempt in range(1, max_attempts + 1):
        try:
            r = requests.post(API_URL, json={"query": question}, timeout=120)
            if r.status_code == 200:
                return 200, r.json().get("response", ""), ""
            body = r.text or ""
            # 500 genérico pode esconder 429 do Vertex; trate como rate-limit se for "Internal Server Error" sem detalhes
            if (r.status_code in (429, 500)) and ( _looks_rate_limited(r.status_code, body) or "INTERNAL SERVER ERROR" in body.upper() ):
                if attempt < max_attempts:
                    wait = backoffs[min(attempt - 1, len(backoffs) - 1)]
                    print(f"↻ rate-limit/500 genérico (tentativa {attempt}/{max_attempts}), aguardando {wait}s…")
                    time.sleep(wait)
                    continue
            return r.status_code, "", body[:400]
        except Exception as e:
            if attempt < max_attempts:
                wait = backoffs[min(attempt - 1, len(backoffs) - 1)]
                print(f"↻ erro '{str(e)[:80]}…' (tentativa {attempt}/{max_attempts}), aguardando {wait}s…")
                time.sleep(wait)
                continue
            return "ERR", "", str(e)[:400]

def main():
    rows = []
    for i, (tid, question, kws, src) in enumerate(TESTS, start=1):
        status, ans, err = call_chat(question)
        if status == 200:
            verdict = _verdict(ans, kws)
            # resposta COMPLETA no CSV (sem corte); normalizo quebras de linha
            answer_field = ans.replace("\r", " ").replace("\n", " ")
            shown = answer_field[:120]  # só para o console
        else:
            verdict = "na" if (isinstance(status, int) and status in (429, 500)) else "fail"
            answer_field = (err or "erro").replace("\r", " ").replace("\n", " ")
            shown = answer_field[:120]

        rows.append([tid, question, "|".join(kws), src, status, verdict, answer_field])
        print(f"{'✓' if verdict=='pass' else '•' if verdict=='partial' else '◦' if verdict=='na' else '×'} {tid} -> {verdict} [{status}] | {shown}")

        # espaça as chamadas
        time.sleep(PER_TEST_SLEEP)
        if i % COOLDOWN_EVERY == 0 and i != len(TESTS):
            print(f"… cooldown de {COOLDOWN_SECONDS}s para aliviar quota …")
            time.sleep(COOLDOWN_SECONDS)

    out = "sauter_site_smoke_results.csv"
    with open(out, "w", newline="", encoding="utf-8-sig") as f:
        w = csv.writer(f, delimiter=";", quotechar='"', quoting=csv.QUOTE_ALL)
        w.writerow(["test_id","question","expected_keywords_any","source_url","http_status","verdict","answer"])
        w.writerows(rows)
    print(f"\nSaved: {out}")

if __name__ == "__main__":
    main()
