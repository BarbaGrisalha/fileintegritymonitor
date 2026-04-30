# File Integrity Monitor

Aplicação em Python para monitorar a integridade de arquivos com hash SHA-256.

## O que faz

- Seleciona um arquivo pelo explorador do sistema
- Calcula o hash SHA-256 do arquivo
- Salva o hash em `hash_data.json`
- Verifica depois se o arquivo foi alterado
- Exibe mensagens de sucesso, erro e alerta na interface gráfica

## Tecnologias usadas

- Python
- `tkinter` da biblioteca padrão
- `hashlib`
- `json`
- `os`

## Estrutura do projeto

```text
FileIntegrityMonitor/
├── fileIntegrityMonitor.py
├── test_fim.py
├── requirements.txt
├── .gitignore
└── README.md
```

## Como executar

Na pasta do projeto:

```bash
python3 fileIntegrityMonitor.py
```

Se o seu Python atual não abrir a janela gráfica, use um Python com suporte a `tkinter`, por exemplo:

```bash
/Library/Frameworks/Python.framework/Versions/3.12/bin/python3 fileIntegrityMonitor.py
```

## Como usar

1. Clique em **Selecionar arquivo**.
2. Escolha um arquivo qualquer.
3. Clique em **Salvar hash**.
4. Depois clique em **Verificar arquivo** para conferir se o conteúdo mudou.

Se o arquivo for alterado depois do salvamento, o programa vai avisar que a integridade foi comprometida.

## Testes

Execute os testes com:

```bash
python3 -m unittest -v test_fim.py
```

## Dependências

O projeto não depende de bibliotecas externas obrigatórias. O arquivo `requirements.txt` existe para documentar isso.

## Arquivos gerados

- `hash_data.json`: salvo quando você usa a opção de salvar hash

Esse arquivo já está no `.gitignore`.

## Observações

- O projeto usa a biblioteca padrão do Python sempre que possível.
- A interface foi escrita para ser simples e fácil de entender, ideal para portfólio e estudo.

## Licença

Projeto pessoal para estudo e portfólio.
