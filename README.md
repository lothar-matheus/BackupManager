# 🔒 Backup Manager

## 📋 Descrição

Este programa permite criar backups de pastas com opção de criptografia, garantindo a segurança e integridade dos dados. Os backups são compactados em formato ZIP e podem ser protegidos com criptografia AES-256.

## ✨ Funcionalidades

- **Backup Simples**: Cria um backup compactado (ZIP) de qualquer pasta
- **Backup Criptografado**: Cria um backup compactado e criptografado com senha
- **Descriptografar Backup**: Descriptografa backups protegidos para restauração

## 🔐 Tecnologias de Segurança

- **Algoritmo de Criptografia**: AES (Advanced Encryption Standard)
- **Derivação de Chave**: SHA-256 hash da senha fornecida
- **Formato**: Fernet (implementação segura do AES-128 em modo CBC)
- **Compressão**: ZIP com DEFLATE

## 📦 Requisitos

- Python 3.7 ou superior
- Biblioteca `cryptography`

## 🚀 Instalação

1. Clone ou baixe este repositório

2. Instale as dependências:
```bash
pip install -r requirements.txt
```

## 💻 Como Usar

1. Execute o programa:
```bash
python backup_manager.py
```

2. Escolha uma das opções do menu:
   - **[1] Backup Simples**: Cria backup sem criptografia
   - **[2] Backup com Criptografia**: Cria backup protegido por senha
   - **[3] Descriptografar Backup**: Restaura um backup criptografado
   - **[0] Sair**: Encerra o programa

### Exemplo de Uso - Backup Simples

```
Digite o caminho completo da pasta para backup: C:\MeusProjetos\ProjetoX
```

O backup será salvo em: `Desktop/backup/ProjetoX_backup_20260205_143022.zip`

### Exemplo de Uso - Backup Criptografado

```
Digite o caminho completo da pasta para backup: C:\MeusProjetos\ProjetoX
Senha: ********
Confirme a senha: ********
```

O backup será salvo em: `Desktop/backup/ProjetoX_backup_20260205_143022.zip.encrypted`

### Exemplo de Uso - Descriptografar

```
Digite o caminho do arquivo criptografado: C:\Users\User\Desktop\backup\ProjetoX_backup_20260205_143022.zip.encrypted
Digite a senha do backup: ********
```

O arquivo descriptografado será salvo no mesmo diretório sem a extensão `.encrypted`

## 📁 Estrutura de Arquivos

```
backup-manager/
│
├── backup_manager.py      # Programa principal
├── requirements.txt       # Dependências do projeto
└── README.md             # Documentação
```

## 🔒 Segurança

### Pontos Fortes
- Criptografia AES-256 através do Fernet
- Hash SHA-256 para derivação de chave
- Validação de senha com confirmação
- Preservação da estrutura original de pastas

### Recomendações de Segurança
- **Senhas Fortes**: Use senhas com pelo menos 12 caracteres
- **Armazenamento Seguro**: Guarde suas senhas em um gerenciador de senhas
- **Backup da Senha**: Sem a senha, não é possível recuperar os dados
- **Teste de Restauração**: Sempre teste a descriptografia após criar um backup

## ⚠️ Avisos Importantes

1. **Não perca sua senha**: Sem ela, os dados criptografados não podem ser recuperados
2. **Guarde backups em locais seguros**: Considere usar múltiplas localizações
3. **Teste regularmente**: Verifique se seus backups podem ser restaurados
4. **Permissões**: O programa precisa de permissões de leitura na pasta de origem

## ⚖️ Uso Responsável e Legal

**IMPORTANTE**: Este projeto foi desenvolvido exclusivamente para fins acadêmicos e educacionais como parte de um portfólio em Segurança da Informação.


**O desenvolvedor não se responsabiliza por uso inadequado desta ferramenta. Use apenas para propósitos legais e éticos.**

## 🎯 Casos de Uso

- Backup de documentos pessoais sensíveis
- Proteção de código-fonte e projetos
- Arquivamento seguro de dados confidenciais
- Conformidade com políticas de segurança da informação

## 📝 Autor

Matheus Lemos

## 📄 Licença

Este projeto está licenciado sob a Licença MIT - veja o arquivo LICENSE para mais detalhes.



---

**Desenvolvido por Matheus Lemos**


**Lembre-se: Use esta ferramenta de forma responsável e apenas para fins legais.**
